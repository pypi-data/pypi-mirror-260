#!/usr/bin/env/pyhton3

"""
Marlin acoustic dataclasses, data adapter, and streamer. 
c. Rahul Tandon, R.S. Aqua, 2024
E: r.tandon@rsaqua.co.uk

Sumamry of classes: 
============================================

---SignatureData--- : 
A DataClass that defines the labelled data downloaded. Labelled data is defined as data that has been analysed and annotated. The process of
annotating data is performed using Marlin Ident. SignatureData represents s an acoustic snapshot that has been identified as a legitimate member of a validation dateset.

---SimulationData--- : 
A DataClass that defines all the acoustic data held in the acoustic database. SignatureData represents an acoustic snapshot.

---MarlinData--- :
Responsible for connecting to and downloading data from the acoustic database. 

---MarlinDataStreamer--- :
Initialised with pointer to SimulationData downloaded data and provides the iterable allowing to easily iterate over the downloaded data.



"""


# --- module imports ---
import re
import glob
import numpy as np
import pandas as pd
import requests, json
import logging
from dotenv import load_dotenv, dotenv_values
import os, sys
from dataclasses import dataclass
import random
from tqdm import tqdm as tq
import scipy
import librosa
from datetime import datetime as dt
from datetime import timedelta
# --- environment setup ---
load_dotenv()
config = dotenv_values("data.env")
# --- logging setup ---
logging.basicConfig(level=logging.CRITICAL)

# --- define custom parms ---
api_server = config['API_SERVER']
api_version = config['API_VERSION']
contact_email = config['CONTACT_EMAIL']



'''
Define data classes. 
'''


@dataclass
class EnergyFrame:
    """
    Energy data frame. 
   
    """
    
    frequency_bounds : list[float]
    time_frame : list[dt]
    energy_measure : float
    id : int
    delta_frequency : float
   
   
@dataclass
class SignatureData:
    """
    Signature dataclass. Define acoustic waveform as a numpy array and pandas dataframe. Dataclass defines a acoustic
    snapshot. meta_data defines snapshot.
    """    

    frequency_ts_np : np.array                  # waveform as numpy array
    frequency_ts_pd : pd.DataFrame              # waveform as dataframe
    meta_data : None                            # snapshot definition
    snapshot : bool = True  
    energy_data_frames : list[EnergyFrame]  = None
    start_time : dt = None
    end_time : dt = None
    
    
@dataclass
class SimulationData:
    """
    Signature dataclass. Define acoustic waveform as a numpy array and pandas dataframe. Dataclass defines a acoustic
    snapshot. meta_data defines snapshot.
    """   
     
    frequency_ts_np : np.array                  # waveform as numpy array
    frequency_ts_pd : pd.DataFrame              # waveform as dataframe
    meta_data : None                             # snapshot definition
    snapshot : bool = True
    energy_data_frames : list[EnergyFrame]  = None
    start_time : dt = None
    end_time : dt = None
    
 
@dataclass
class Multithread:
    """
    Multithread dataclass. Defines data required for multithread compatibility.

  
    """
    mt_snapshot_ids : {}
    number_threads  : int
    
    

'''
Define Classes
'''


class MarlinData(object):
    
    """
    Class to connect and download data from acoustic database.
    """    
    
    def __init__(self, load_args : {} = {}):
        """
        Initialise class object.

        Args:
            load_args (dict, optional): Initialisation arguments : 'limit' | max number of downloads . Defaults to {}.
        """          
    
        self.snapshot_ids = []              # list of signature snapshot ids
        self.sim_snapshot_ids = []          # list of sim snapshot ids
        self.run_ids = []                   # list of run ids
        self.signature_ids = []             # list of signature ids
        self.number_runs = 0                # number of runs in signature data
        self.number_signatures = 0          # number of signatures in data set
        self.number_snapshots = 0           # number of sig snapshots      
        self.number_sim_snapshots = 0       # number of sim snapshots

        self.signature_data = {}            # signature data. Dictionary of SignatureData.
        self.signature_index = []           # index of signature id required as keys
        self.simulation_data = {}           # simulation data. Dictionary of SimulationData.
        self.simulation_index = []          # index of simulation id require as keys
        
        # define default limit
        
        if 'limit' in load_args:
            self.limit_sig = load_args['limit']
        else:
            self.limit_sig = 5
    
    def init_multithread(self, number_threads, load_args):
        """
        Initialise multithread data. Returns array of snapshot ids discretised into number of threads which can 
        be loaded for download.

        Args:
            number_threads (_type_): _description_
            load_args (_type_): _description_

        Returns:
            _type_: _description_
        """
        
        snapshot_endpoint = "data/snapshot/data/all"
        api_url = f"{api_server}/rs/api/v{api_version}/{snapshot_endpoint}"
        
        try:
            r = requests.get(api_url) 
            request_json_data_signature = r.json()['data']
            # number_r = len(request_json_data_signature)
            
        except Exception as ex:
            logging.critical(f"[marlin_data.py] Unable to run signature retrieval api request. Email {contact_email} | {ex}")

        
        # download_limit = number_r // number_threads
        download_cnt = 0
        thread_counter = 0
        snapshot_id_holder = {}
        snapshot_id_list = []
        number_r = 0
        for snapshot in request_json_data_signature:
            
           
            if 'location' in load_args:
                if snapshot['data_receiver_location_name'] in load_args['location']:
                    number_r += 1
                    snapshot_id_list.append(snapshot['ss_id'])
                    
        
        download_limit = number_r // number_threads
        snapshot_id_list_mt = []
        for snapshot_id in snapshot_id_list:   
            snapshot_id_list_mt.append(snapshot_id)
            download_cnt += 1
            if download_cnt >= download_limit:
                download_cnt = 0
                snapshot_id_holder[thread_counter] = snapshot_id_list_mt
                thread_counter += 1
                
        return_data = Multithread(snapshot_id_holder, thread_counter)
        return return_data
             
    def download_signature_snapshots(self, load_args : {} = {}) -> ({}):
        
        if 'limit' in load_args:
            self.limit_sig = load_args['limit']
        """Load binary data from RSA server and load into corresponding dataclasses.

        Args:
            load_args (dict, optional): Load arguments. E.g.location contraints. Defaults to {}.

        Returns:
            {}, [] | {key : snapshot_id , value : signature dataclass} , [snapshot_id]
        """   
        
        signature_enpoint = "data/signature"
        api_url = f"{api_server}/rs/api/v{api_version}/{signature_enpoint}"
        
        try:
            r = requests.get(api_url) 
            request_json_data_signature = r.json()['data']

        except Exception as ex:
            logging.critical(f"[marlin_data.py] Unable to run signature retrieval api request. Email {contact_email} | {ex}")

        for signature in request_json_data_signature:
            
             
          
            if signature['snapshot_id'] not in self.snapshot_ids:
                self.snapshot_ids.append(signature['snapshot_id'])
                
            if signature['run_id'] not in self.run_ids:
                self.run_ids.append(signature['run_id'])
                
            if signature['signature_id'] not in self.signature_ids:
                self.signature_ids.append(signature['signature_id'])
            
        
       
        # limit_sig = 5
        limit_sig_cnt = 1
        
        for snapshot_id in self.snapshot_ids:
            
            if limit_sig_cnt > self.limit_sig:
                break
            # -- 
            # We have the signature id now and require snapshot data in order to build metadata, e.g. delta t, time and location id.
            # We now grab all the meta data for the signature
            # --
           
            
            # get the snapshot id of the snapshot xr with signature
            # snapshot_id = signature['snapshot_id']
            snapshot_id = snapshot_id            
            #define API endpoint & url
            snapshot_data_signature_enpoint = "data/snapshot/data"
            snapshot_data_signature_url = f"{api_server}/rs/api/v{api_version}/{snapshot_data_signature_enpoint}/{snapshot_id}"
            # print (snapshot_data_signature_url)
            
            
            # make api request
            try:
                
                r_ss = requests.get(snapshot_data_signature_url) 
                request_json_data_snapshot = r_ss.json()['data'][0]
                
                #---
                # Filter Snapshots
                #---
                
                if 'ss_ids' in load_args:
                    if request_json_data_snapshot['ss_id'] not in load_args['ss_ids']:
                        continue
                
                if 'location' in load_args:
                    # print (signature)
                    
                    print (request_json_data_snapshot['data_receiver_location_name'], load_args['location'])
                    if request_json_data_snapshot['data_receiver_location_name'] not in load_args['location']:
                        
                        continue
            
               
                
                # print (request_json_data_snapshot)
                meta_data = self.parse_meta(snapshot_data = request_json_data_snapshot)
                
                
                
                
            except Exception as ex:
                logging.debug(f"[marlin_data.py - 2] Unable to run snapshot data retrieval api request. Email {contact_email} | {ex}")
    
            # --
            # Get serial data : meta data complete, download and convert the stored serial data
            # --
            
            #define API endpoint & url
            snapshot_data_signature_enpoint = "data/snapshot/serialdata"
            snapshot_serial_data_url = f"{api_server}/rs/api/v{api_version}/{snapshot_data_signature_enpoint}/{snapshot_id}"
            
            # make api request & load
            try:
                
                r_serial = requests.get(snapshot_serial_data_url) 
                
                request_json_serial_data = r_serial.json()['data'][0]
                
                if 'signature_path' not in load_args.keys():
                    
                    load_args['signature_path'] = ""
                    
                domain_data_np, domain_data_pd = self.deserial_data(raw_data = request_json_serial_data['json_raw'], path=load_args['signature_path'], meta_data = meta_data)
                # meta_data = self.parse_meta(snapshot_data = request_json_data_snapshot)
                
                
                sim_data = SignatureData(frequency_ts_np = domain_data_np, frequency_ts_pd = domain_data_pd, meta_data = meta_data)
                
                
              
                self.signature_data[snapshot_id] = sim_data
                
                self.signature_index.append(snapshot_id)
                limit_sig_cnt += 1
                
                
                
                # if domain_data_np or domain_data_pd == None:
                #     logging.debug(f"[marlin_data.py -3] {snapshot_id} Empty serial data file for snapshot raw data.Email {contact_email} ")
                    
                
            except Exception as ex:
                logging.debug(f"[marlin_data.py - 5] Unable to run snapshot data retrieval api request. Email {contact_email} | {ex}")
    
            

        # set length parameters
        self.number_runs = len(self.run_ids)
        self.number_snapshots = len(self.snapshot_ids)
        self.number_signatures = len(self.signature_index)
        
        return self.signature_data, self.signature_index
             
    def download_simulation_snapshots(self, load_args = {}) -> ({}):
        """Load binary data from RSA server and load into corresponding dataclasses.

        Args:
            load_args (dict, optional): _description_. Defaults to {}.

        Returns:
            {}, []: {key : snapshot_id , value : simulation dataclass} , [snapshot_id]
        """   
        
        if 'limit' in load_args:
            self.limit_sig = load_args['limit']
        
        snapshot_endpoint = "data/snapshot/data/all"
        api_url = f"{api_server}/rs/api/v{api_version}/{snapshot_endpoint}"
        
        request_json_data_snapshots = None
        try:
            r = requests.get(api_url) 
            
            request_json_data_snapshots = r.json()['data']

        except Exception as error:
            logging.critical(f"{error}")
        
            logging.critical(f"[marlin_data.py] Unable to run all snapshots retrieval api request. Email {contact_email}")
        
        
        
        limit_sig_cnt = 1
        for snapshot in request_json_data_snapshots:
            if limit_sig_cnt > self.limit_sig:
               
                break
            # --
            # Build tag and id trackers for data object
            # --
            # logging.debug(load_args['ss_ids'])
            
            # logging.debug(f'ss_id{snaphsot['ss_id']}')
            # Filter---
           
            if 'ss_ids' in load_args:
                if snapshot['ss_id'] not in load_args['ss_ids']:
                    
                    continue
            if 'location' in load_args:
                
                if snapshot['data_receiver_location_name'] not in load_args['location']:
                    
                    continue
            # ----
            
            if snapshot['ss_id'] not in self.sim_snapshot_ids:
                self.sim_snapshot_ids.append(snapshot['ss_id'])
                limit_sig_cnt += 1
            # if snapshot['run_id'] not in self.run_ids:
            #     self.sim_run_ids.append(signature['run_id'])
                
        
           
        
        for snapshot_id in self.sim_snapshot_ids:
           
            # -- 
            # We have the signature id now and require snapshot data in order to build metadata, e.g. delta t, time and location id.
            # We now grab all the meta data for the signature
            # --
            
            
            
            # get the snapshot id of the snapshot xr with signature
            # snapshot_id = signature['snapshot_id']
            snapshot_id = snapshot_id            
            #define API endpoint & url
            snapshot_data_signature_enpoint = "data/snapshot/data"
            snapshot_data_signature_url = f"{api_server}/rs/api/v{api_version}/{snapshot_data_signature_enpoint}/{snapshot_id}"
            
            
            # make api request
            try:
                r_ss = requests.get(snapshot_data_signature_url) 
                request_json_data_snapshot = r_ss.json()['data'][0]
                
                #filter location
                
                    
                
                meta_data = self.parse_meta(snapshot_data = request_json_data_snapshot)
               
            except Exception as ex:
                logging.critical(f"[marlin_data.py - 2] Unable to run snapshot data retrieval api request. Email {contact_email} | {ex}")
    
            # --
            # Get serial data : meta data complete, download and convert the stored serial data
            # --
            
            #define API endpoint & url
            snapshot_data_signature_enpoint = "data/snapshot/serialdata"
            snapshot_serial_data_url = f"{api_server}/rs/api/v{api_version}/{snapshot_data_signature_enpoint}/{snapshot_id}"
            
            # make api request
            try:
                
                r_serial = requests.get(snapshot_serial_data_url)
                try: 
                    request_json_serial_data = r_serial.json()['data'][0]
                    
                except Exception as ex:
                    logging.critical(f'Exception raised: {ex}')
                    continue
                
                if "success" in r_serial.json()['data'][0]:
                    continue
                    
                if 'simulation_path' not in load_args.keys():
                    load_args['simulation_path'] = ""
                
                domain_data_np, domain_data_pd = self.deserial_data(raw_data = request_json_serial_data['json_raw'], path=load_args['simulation_path'],meta_data= meta_data)
                sig_data = SimulationData(frequency_ts_np = domain_data_np, frequency_ts_pd = domain_data_pd, meta_data = meta_data)
                self.simulation_data[snapshot_id] = sig_data
                self.simulation_index.append(snapshot_id)
                # if domain_data_np or domain_data_pd == None:
                #     logging.debug(f"[marlin_data.py -3] {snapshot_id} Empty serial data file for snapshot raw data.Email {contact_email} ")
                    
                
            except Exception as ex:
                logging.critical(f"[marlin_data.py - 5] Unable to run snapshot data retrieval api request. Email {contact_email} | {ex}")
    

        # set lenght parameters
        self.number_sim_snapshots = len(self.sim_snapshot_ids)
        
        return self.simulation_data, self.simulation_index
    
    def get_track_data(self, mmsi : int = 0, lander_loc : str = "", approach_radius : float =0.0, start_time : str = "", end_time : str = ""):
        '''
            Get a list of snapshot ids from mmsi of vessel. approaches. Check validity and XR with existing data. Use Marlin API
        '''
        
        self.approaches = []
        
        lander_pos = {}
        lander_pos['netley'] = {'lat' : 50.871, 'long' : -1.373}
        lander_lat = lander_pos[lander_loc]['lat']
        lander_long = lander_pos[lander_loc]['long']
        
        url = f'https://vixen.hopto.org/rs/api/v1/data/ships/tracks/{mmsi}/target_known/{lander_lat}/{lander_long}/{approach_radius}'
        
        track_data = None
        try:
            r = requests.get(url) 
            track_data = r.json()
            number_approaches = track_data['number_of_approaches']
            number_tracks = track_data['number_tracks']

        except Exception as ex:
            logging.critical(f"[marlin_data.py] Unable to run signature retrieval api request. Email {contact_email} : {ex}")

        # for each approach create a vector of snapshot ids.
        for approach_id in range(0,number_approaches):
            
            start_time = track_data['approach_profiles'][approach_id][0]['time']
            end_time = track_data['approach_profiles'][approach_id][len(track_data['approach_profiles'][approach_id])-1]['time']
            
            session_id = random.randrange(0,99999)
            post_data = {
                "start_time": start_time,
                "end_time": end_time,
                "location": lander_loc,
                "session_id": session_id,
                "track": "true"
            };
           
            
        
            valid_url =url = "https://vixen.hopto.org/rs/api/v1/data/valid/"
            valid_r = requests.post(valid_url, json.dumps(post_data)) 
            valid_data = valid_r.json()
            snapshot_ids = valid_data['snapshot_ids']
            percent_cover = min(valid_data['percentage_complete'], 100)
            
            # build approach profile data
            approach_profile = track_data['approach_profiles'][approach_id]
            
            
            
            self.approaches.append({'snapshot_ids' : snapshot_ids, 'percent_cover' : percent_cover, 'mmsi' : mmsi, 'approach_profile' : approach_profile})

        return self.approaches
    
    def parse_meta(self, snapshot_data : {} = None) -> {}:
        
        """
        Parse query return of snapshot data into metadata

        Returns:
            {}: MetaData of snapshot.
        """        
        
        meta_data = {}
        meta_data['snapshot_id '] = snapshot_data['ss_id']
        meta_data['snapshot_id'] = snapshot_data['ss_id']
        meta_data['data_frame_start'] = snapshot_data['data_frame_start']
        meta_data['data_frame_end'] = snapshot_data['data_frame_end']
        meta_data['listener_location'] = snapshot_data['data_receiver_location']
        meta_data['location_name'] = snapshot_data['data_receiver_location_name']
        meta_data['frame_delta_t'] = snapshot_data['data_delta_time']
        meta_data['sample_rate'] =  snapshot_data['sample_rate']
        return meta_data
    
    def load_from_path(self, load_args : {} = None):
        
        load_limit = 5
        load_cnt = 1
        if 'limit' in load_args.keys():
            load_limit = load_args['limit']
        
        
        path = load_args['load_path']
        files = glob.glob(f'{path}/*')
        pat = r'.*\_(.*)\..*'    
        processed_snapshots = []
        snapshot_times = {}
        for file in files:
            
            np_data, pd_data, c = (None, None, None)
            
            search_result = re.match(pat, file)
            snapshot_id = search_result.group(1)
            data_filepath = f'{path}/streamedfile_{snapshot_id}.dat'
            metadata_filepath = f'{path}/metadata_{snapshot_id}.json'
            
            if snapshot_id not in processed_snapshots:
                
                processed_snapshots.append(snapshot_id)
                
                with open(data_filepath, 'rb') as fr:
                    c = fr.read()
                    
                dtype = np.dtype("float32")
                np_data  = np.frombuffer(c, dtype=dtype)
                pd_data = pd.DataFrame(np_data)
                fr.close()
                
                with open(metadata_filepath, 'rb') as fr:
                    meta_data = json.load(fr)
                
                start_t_dt = dt.strptime(meta_data['data_frame_start'], '%y%m%d_%H%M%S.%f')
                snapshot_times[start_t_dt] = snapshot_id
                
                if load_args['snapshot_type'] == "simulation":
                    
                    sig_data = SimulationData(frequency_ts_np = np_data, frequency_ts_pd = pd_data, meta_data = meta_data)
                    self.simulation_data[snapshot_id] = sig_data
                    # self.simulation_index.append(snapshot_id)
                    
                else:
                    
                    sig_data = SignatureData(frequency_ts_np = np_data, frequency_ts_pd = pd_data, meta_data = meta_data)
                    self.signature_data[snapshot_id] = sig_data
                    # self.signature_index.append(snapshot_id)
        
                load_cnt += 1
                if load_cnt >= load_limit:
                    break
        
        # rearrange index vector wrt time
        
        dates_sorted = sorted(snapshot_times.keys())
        for time_ in dates_sorted[0:load_limit-1]:
            
            if load_args['snapshot_type'] == "simulation":
                snapshot_id = snapshot_times[time_]
                self.simulation_index.append(snapshot_id)
                
            if load_args['snapshot_type'] == "signature":
                snapshot_id = snapshot_times[time_]
                self.signature_index.append(snapshot_id)
                
            
        # for id, time in snapshot_times.items():
        #     print (time)
        
    def build_game(self):
        """
            Add signature / labelled data to the simulation mix in order to ensure we have labelled data in the simulation.
        """
        # --- add siganture snapshots to simulation game if not already present
        for sig_snap_id in self.signature_index:
            if sig_snap_id  not in self.simulation_index:
                self.simulation_index.append(sig_snap_id)
                self.simulation_data[sig_snap_id] = self.signature_data[sig_snap_id]
        
        # --- re order snapshot ids into chronological order
        snapshot_times = {}
        for snapshot in self.simulation_data:
            start_t_dt = dt.strptime(snapshot.meta_data['data_frame_start'], '%y%m%d_%H%M%S.%f')
            snapshot_times[start_t_dt] = snapshot.metadata['snapshot_id']
            
        dates_sorted = sorted(snapshot_times.keys())
        # clear index
        self.simulation_index = []
        # rebuild index
        
        for time_ in dates_sorted:
            snapshot_id = snapshot_times[time_]
            self.simulation_index.append(snapshot_id)
     
    def deserial_data(self, raw_data : {} = None, path : str = "", meta_data : {} = None) -> (np.array, pd.DataFrame):
        """
        Read/stream remote serial data and load into a readable format / data structure.

        Args:
            raw_data from a snapshot data query from Marlin API

        Returns:
            np.array, pd.DataFrame
        """        
        
        np_data, pd_data, c = (None, None, None)
        
        random_tag = meta_data['snapshot_id']
        # pandas_data = None
        # c = None
        if 'raw_data_url' in raw_data:
            
            
            filepath = ""
            if path == "":
                filepath = f'streamedfile_{random_tag}.dat'
                json_filepath = f'metadata_{random_tag}.json'
            else:
                filepath = f'{path}/streamedfile_{random_tag}.dat' 
                json_filepath =  f'{path}/metadata_{random_tag}.json' 

            with open(json_filepath, 'w') as f_:
                json.dump(meta_data, f_)

            serial_domain_data_fn = raw_data['raw_data_url']
           
            r = requests.get(serial_domain_data_fn, allow_redirects=True, stream=True)
            
            total_length = r.headers.get('content-length')
            
            print (f"[Marlin Data : Fetching binary data : {serial_domain_data_fn}]")
           
            # f = open(f'streamed_file{random_tag}', 'wb')
            f = open(filepath, 'wb')
            dl = 0
            total_length = int(total_length)
            
            for data in r.iter_content(chunk_size=2000):
                dl += len(data)
                f.write(data)
                done = int(50* dl / total_length)
                sys.stdout.write("\r[%s%s]" % ('=' * done, ' ' * (50-done)))
                sys.stdout.flush()

            sys.stdout.flush()

            
            # with open(f'streamed_file{random_tag}', 'rb') as fr:
            #     c = fr.read()
            with open(filepath, 'rb') as fr:
                c = fr.read()
                
            dt = np.dtype("float32")
            np_data  = np.frombuffer(c, dtype=dt)
            pd_data = pd.DataFrame(np_data)
            fr.close()

            
        return np_data, pd_data
      
    def build_derived_data(self, n_fft : int = 1024):
        self.derived_data = MarlinDerivedData(n_fft=n_fft)
        
             
class MarlinDataStreamer(object):
    """
    Class to connect to MarlinData and provide an iterable for data access.

    
    """   
    def __init__(self):
       
        self.data_feed = {}
        self.data_ids = []
        self.feed_index = -1
        self.data_vec_length = 0
    
    def init_data(self, data_feed : {} = {}, data_ids : [] = []) -> None:
        """_summary_

        Args:
            data_feed ({}, optional): Dataclass structure and key. Defaults to {}.
            data_ids ([], optional): keys. Defaults to [].
        """        
        # initiaslise vector of feed epoch ids
        self.data_ids = data_ids
        
        # initialise the feed dataset
        self.data_feed = data_feed
        
        # determin lenght of data feed
        self.data_vec_length = len(self.data_ids)
        
        # start data feed
        self.feed_index = 0
        
    def get_data(self, data_idx : int = 0):
        return self.data_feed[data_idx]
    
    def __iter__(self):
        return self
        
    def __next__(self):
        if self.feed_index >= self.data_vec_length:
            self.feed_index = 0
            raise StopIteration
        
        feed_value = self.data_feed[self.data_ids[self.feed_index]]
        self.feed_index += 1
        return feed_value


class MarlinDerivedData(object):
    '''
    Define data derived from energy time series
    '''

    def __init__(self, n_fft : int = 2048):
        """
        Initialise Class

        Args:
            n_fft (int, optional): Fourier frame size. Defaults to 1024.
        """
        self.n_fft = n_fft  
        self.energy_frames = []         # global energy_frames
        self.sample_times = []          # sample times from fft
        self.model_sample_times = []    # sample times for model
        self.data_start_time = None     # time bounds for data
        self.data_end_time = None       # time bounds for data
        self.number_energy_frames = 0   # number of energy data frames

        self.labelled_data = {}         # data_structure to xr labelled data with
        
    def build_derived_data(self, simulation_data : SimulationData = None, sample_delta_t : float = 0.5):
        """
        

        Args:
            signature_data (SignatureData, optional): _description_. Defaults to None.
        """
        
        '''
        Build derived data from raw energy time series. 
        1. perform fft on dataset -> f and t bins
        '''
        
        # --- run sft on data --
        raw_data = simulation_data.frequency_ts_np
        hop_length = self.n_fft // 2
        
        D = librosa.amplitude_to_db(np.abs(librosa.stft(raw_data, n_fft=self.n_fft, hop_length=hop_length)), ref=np.max)
        
        # --- get frequemcies and time ranges ---
        librosa_time_bins = librosa.frames_to_time(range(0, D.shape[1]), sr=simulation_data.meta_data['sample_rate'], hop_length=(self.n_fft//2), n_fft=self.n_fft)
        librosa_f_bins = librosa.core.fft_frequencies(n_fft=self.n_fft, sr=simulation_data.meta_data['sample_rate'])
        
        # time considerations
        signature_frame_start_dt = dt.strptime(simulation_data.meta_data['data_frame_start'], '%y%m%d_%H%M%S.%f')
        signature_frame_end_dt = dt.strptime(simulation_data.meta_data['data_frame_end'], '%y%m%d_%H%M%S.%f')
        marlin_sample_time = sample_delta_t  #seconds
        marlin_sample_time_dt = timedelta(seconds = marlin_sample_time)
        
        simulation_data.start_time = signature_frame_start_dt
        simulation_data.end_time = signature_frame_end_dt
        
        
        
        # --- build time reference vector
        librosa_time_bins_dt = list (map(lambda v : signature_frame_start_dt +  timedelta(seconds=v), librosa_time_bins))
        # librosa_time_bins_dt.sort()
        self.sample_times.extend(librosa_time_bins_dt) 
        self.sample_times.sort()
        self.data_start_time = self.sample_times[0]
        self.data_end_time = self.sample_times[len(self.sample_times)-1]
        # self.build_sample_time_vector(librosa_time_bins)
        # self.sample_times = list(map(lambda i, v : signature_frame_start_dt + timedelta(seconds=((v[i]-v[i-1])/2)),enumerate(librosa_time_bins[1:len(librosa_time_bins)])))
        # self.sample_times = list (map(lambda v : (v[1]-v, enumerate(librosa_time_bins)))
        # # --- build energyframes ---
        
        
        # iterate over time bins and build energy datastructures
        self.max_freq = 0
        self.min_freq = 99999
        self.max_energy = 0
        self.delta_frequency = 0
        energy_frames = []
        _id = 0
        for freq_idx in range(1,len(librosa_f_bins)-1):
            
            self.max_freq = max(self.max_freq, librosa_f_bins[freq_idx] )
            self.min_freq = min(self.min_freq, librosa_f_bins[freq_idx] )
            for sample_time_idx in range(1, len(librosa_time_bins)-1):
                energy = D[freq_idx, sample_time_idx]
                self.max_energy = max(self.max_energy, energy)
                sample_time_start = signature_frame_start_dt + timedelta(seconds=librosa_time_bins[sample_time_idx-1])
                sample_time_end = signature_frame_start_dt + timedelta(seconds=librosa_time_bins[sample_time_idx])
                
                # create energy frame
                delta_f = librosa_f_bins[freq_idx] - librosa_f_bins[freq_idx-1]
                self.delta_frequency = delta_f
                ef = EnergyFrame(frequency_bounds=[librosa_f_bins[freq_idx-1], librosa_f_bins[freq_idx]], time_frame=[sample_time_start, sample_time_end], energy_measure=energy, id=_id, delta_frequency = delta_f)
                
                # add energy frame to list of energy frames
                energy_frames.append(ef)
                self.energy_frames.append(ef)
                _id += 1 
            
            
        simulation_data.energy_data_frames = energy_frames
        self.number_energy_frames = len(energy_frames)
      
    def build_derived_labelled_data(self, signature_data : SignatureData = None):
        """
        Build structure of signature time frames
        nb. resolution will be an issue here.
        This data structure is used to query validity of decision values in optimisation.
        Args:
            signature_data (SignatureData, optional): _description_. Defaults to None.
        """
        # update time frame of signature
        signature_frame_start_dt = dt.strptime(signature_data.meta_data['data_frame_start'], '%y%m%d_%H%M%S.%f')
        signature_frame_end_dt = dt.strptime(signature_data.meta_data['data_frame_end'], '%y%m%d_%H%M%S.%f')
        signature_data.start_time = signature_frame_start_dt
        signature_data.end_time = signature_frame_end_dt 
        time_bounds = [signature_data.start_time, signature_data.end_time]
        self.labelled_data[str(signature_data.meta_data['snapshot_id'])] = time_bounds
      
      
        
            
    def query_energy_frames_at_time(self, _time : dt, data_instance : SimulationData = None):
        """
        
        Query energy frames by frequency bounds. 

        Args:
            time (dt): _description_
            frequency (float): _description_
            data_instance (SimulationData): _description_

        Returns:
              [EnergyFrame]: List of valid energy frames, float : average energy value
        """
        energy_frames = []
        if data_instance is not None:
            for energy_data in data_instance.energy_data:
                if _time >= energy_data.time_frame[0] and _time <= energy_data.time_frame[1]:
                    energy_frames.append(energy_data)
        else:
            energy_frames = self.energy_frames
    
        energy_sum = 0
        for energy_frame in energy_frames:
            energy_sum += energy_frame.energy_measure
        
        avg_energy = energy_sum/max(1,len(energy_frames))
        
            

        return energy_frames, avg_energy
    
    def query_energy_frames_at_frequency(self, frequency: float, data_instance : SimulationData = None, _time : dt = None):
        """
        
        Query energy frames by frequency bounds and time bounds
    
        Args:
            time (dt): _description_
            frequency (float): _description_
            data_instance (SimulationData): _description_

        Returns:
            [EnergyFrame]: List of valid energy frames, float : average energy value
        """
        
        energy_frames = []
        if _time is not None:
            if data_instance is not None:
                for energy_data in data_instance.energy_data:
                    if frequency >= energy_data.frequency_bounds[0] and frequency <= energy_data.frequency_bounds[1]  and (energy_data.time_frame[0] <= _time and energy_data.time_frame[1] >= _time):
                        energy_frames.append(energy_data)
            else:
                for energy_data in self.energy_frames:
                    # print (energy_data.frequency_bounds[0],energy_data.frequency_bounds[1] )
                    # print (energy_data.time_frame[0])
                    
                    if frequency >= energy_data.frequency_bounds[0] and frequency <= energy_data.frequency_bounds[1] and energy_data.time_frame[0] <= _time and energy_data.time_frame[1] >= _time:
                        # print ("here")
                        energy_frames.append(energy_data)
                    
        if _time is None:
            if data_instance is not None:
                for energy_data in data_instance.energy_data:
                    if frequency >= energy_data.frequency_bounds[0] and frequency <= energy_data.frequency_bounds[1]:
                        energy_frames.append(energy_data)
            
            else:
                for energy_data in self.energy_frames:
                    if frequency >= energy_data.frequency_bounds[0] and frequency <= energy_data.frequency_bounds[1]:
                        energy_frames.append(energy_data)
    
    
    
        energy_sum = 0
        for energy_frame in energy_frames:
            energy_sum += energy_frame.energy_measure
        
        avg_energy = energy_sum/max(1,len(energy_frames))
        return energy_frames, avg_energy
    
    def query_energy_frames_at_frequency_bounds(self, frequency_min: float, frequency_max: float, _time : dt = None):
        """

        Args:
            frequency_min (float): _description_
            frequency_max (float): _description_
            _time (dt, optional): _description_. Defaults to None.

        Returns:
            _type_: _description_
        """
        
        energy_frames = []
        if _time is not None:
           
                for energy_data in self.energy_frames:
                    
                    
                    if energy_data.frequency_bounds[0] >= frequency_min and energy_data.frequency_bounds[1] <= frequency_max and energy_data.time_frame[0] <= _time and energy_data.time_frame[1] >= _time:
                        # print ("here")
                        energy_frames.append(energy_data)
                    
        if _time is None:
           
                for energy_data in self.energy_frames:
                    if energy_data.frequency_bounds[0] >= frequency_min and energy_data.frequency_bounds[1] <= frequency_max:
                        energy_frames.append(energy_data)
    
    
    
        energy_sum = 0
        for energy_frame in energy_frames:
            energy_sum += energy_frame.energy_measure
        
        avg_energy = energy_sum/max(1,len(energy_frames))
        return energy_frames, avg_energy
    
    def query_energy_frames_at_times_bounds(self, time_start: dt, time_end: dt):
        """
        

        Args:
            time_start (dt): _description_
            time_end (dt): _description_

        Returns:
            _type_: _description_
        """
        
        energy_frames = []
        
           
        for energy_data in self.energy_frames:
            
            
            if energy_data.time_frame[0] >= time_start and energy_data.time_frame[1] <= time_end:
                energy_frames.append(energy_data)


        energy_sum = 0
        for energy_frame in energy_frames:
            energy_sum += energy_frame.energy_measure
        
        avg_energy = energy_sum/max(1,len(energy_frames))
        return energy_frames, avg_energy
    
    def query_energy_frequency_time_bounds(self, time_start: dt, time_end: dt, frequency_min: float, frequency_max: float):
        """
        

        Args:
            time_start (dt): _description_
            time_end (dt): _description_
            frequency_min (float): _description_
            frequency_max (float): _description_

        Returns:
            _type_: _description_
        """
        energy_frames = []
        for energy_data in self.energy_frames:
                    
                    if energy_data.frequency_bounds[0] >= frequency_min and energy_data.frequency_bounds[1] <= frequency_max and energy_data.time_frame[0] >= time_start and energy_data.time_frame[1] <= time_end:
                        energy_frames.append(energy_data)
    
        energy_sum = 0
        for energy_frame in energy_frames:
            energy_sum += energy_frame.energy_measure
        
        avg_energy = energy_sum/max(1,len(energy_frames))
        return energy_frames, avg_energy
    
    def query_label_time(self, time_start: dt, time_end : dt):
        """
        Query for labelled data in a time frame
        Args:
            time_start (dt): _description_
            time_end (_type_): _description_
            dt (_type_): _description_

        Returns:
            _type_: _description_
        """
        xr_data = {"xr":False}
        #math by time rahter than snapshot ids for scalablity / differeing resolutions
        for snapshot_id, time_bounds in self.labelled_data.items():
            if time_start >= time_bounds[0] and time_end <= time_bounds[1]:
                xr_data = {
                    "xr"                : True,
                    "xr_time_start"     : time_start,
                    "xr_time_end"       : time_end,
                    "label_snapshot_id" : snapshot_id
                }
                
                return (xr_data)
    
        return xr_data
    
    def query_label_id(self, snapshot_id : str = ""):
        if snapshot_id in self.labelled_data.keys():
            return True
    
    def __str__(self):
        
        return(f'[Max Frequency] : {self.max_freq} [Min Frequency] : {self.min_freq}')
        


if __name__ == "__main__":
    
    """--- Tutorial / Quick Start ---
    Download both signature data & run data for use in a ML / simulation setup.
    """
    
    # # 1. instantiate a Marlin Data object
    marlin_data = MarlinData(load_args={'limit' : 100000})
    # # 2. download signatures from RSA signature database
    # #marlin_data.download_signatures()
    # # 3. download simulation / ML run snapshot data
    # # marlin_data.download_simulation_snapshots()
    # # src_data_snapshots = [525010]
    # # 4. create a datafeed from the downloaded snapshot data
    # # data_feed = MarlinDataStreamer(load_args = {'location' : 'clyde_surfer_', 'ss_ids' : src_data_snapshots})
    # # data_feed.init_data(marlin_data.simulation_data, marlin_data.simulation_index)
    
    # # # 5. access and print data feed
    # # for data_inst in data_feed:
    # #     print (data_inst)
    
    #---
    
    # target_mmsi = 235078536
    # # # start_time = "2019-12-13 14:04:38"
    # # end_time = "2019-12-13 14:08:38"
    # # marlin_data.get_track_data(mmsi, 'netley', 0.5)
    # # for approach in marlin_data.approaches:
    # #     print (approach)
    # # src_data_snapshots = [525010, 649540]

    # #download simulation snapshots using the list of snapshot ids as a parameter
    # # marlin_data.download_simulation_snapshots(load_args = {'ss_ids' : src_data_snapshots})
    
    # marlin_data.get_track_data(mmsi=target_mmsi, lander_loc='netley', approach_radius=0.5)

    # for approach in  marlin_data.approaches:
    #     # only look for approaches with majority cover
    #     if approach['percent_cover'] > 50:
    #         print (approach['approach_profile'])
    #         # convert to integers
    #         # approach_snapshot_ids = list(map(int,approach['snapshot_ids']))
    #         # print (approach_snapshot_ids)
    #         # marlin_data.download_simulation_snapshots(load_args={'ss_ids' : approach_snapshot_ids} )
            
    # download signature data
      
    # # buid derive data structure
    # marlin_data.build_derived_data(n_fft=2048)
    
    # # 4. create a datafeed from the downloaded snapshot data
    # data_feed = MarlinDataStreamer()
    # data_feed.init_data(marlin_data.simulation_data, marlin_data.simulation_index)

    # # 5. access and print data feed
    # for data_inst in data_feed:
    #     marlin_data.derived_data.build_derived_data(data_inst)
    #     # sample_date_time = data_inst.energy_data[0].time_frame[0].strftime("%y%m%d_%H%M%S.%f")
    #     # sample_date_time = dt.strptime("181020_093455.011333", "%y%m%d_%H%M%S.%f")
    #     # #181020_093455.001333
    #     # energy_data = marlin_data.derived_data.query_energy(_time=sample_date_time, data_instance = data_inst)
        
    # # for data_inst in data_feed:
    #     # for energy_frame in data_inst.energy_data_frames:
    #         # print (f'energy measure : {energy_frame.energy_measure}')
    # print ("\n")
    # print (f'Data start time : {marlin_data.derived_data.data_start_time} End time : {marlin_data.derived_data.data_end_time}')
    # print (f'Number of energy frames : {marlin_data.derived_data.number_energy_frames}')
    # print (f'Maximum f : {marlin_data.derived_data.max_freq}')
    # print (f'Minimum f : {marlin_data.derived_data.min_freq}')
    # print (f'Delta f : {marlin_data.derived_data.delta_frequency}')
    
    # for t in marlin_data.derived_data.sample_times:
    #     #2018-10-20 09:35:04.180667
    #     # print (f'Getting Energy at {t} for {freq} Hz')
    #     t_end = t + timedelta(seconds = 1)
    #     frames, energy = marlin_data.derived_data.query_energy_frequency_time_bounds(t, t_end, 2000,2500)
    #     print (f"<E> {energy}")
    #     print (f'Number of energy frames : {len(frames)}')
    #     exit()
        
        
        

    # marlin_data.download_signature_snapshots(load_args={'signature_path' : "test"})
    # marlin_data.build_derived_data(n_fft=2048)
    # data_feed = MarlinDataStreamer()
    # data_feed.init_data(marlin_data.signature_data, marlin_data.signature_index)
    
    # for data_inst in data_feed:
    #     print (data_inst.frequency_ts_np)
    #     marlin_data.derived_data.build_derived_labelled_data(signature_data=data_inst)
    
    # path = "/home/vixen/rs/data/acoustic/ellen/raw_repo/model_snaps"
    # marlin_data.download_simulation_snapshots(load_args = {'location' : ['clyde_surfer_1'], 'limit':1000000000,'simulation_path' : path})
    # # sim_data_feed = MarlinDataStreamer()
    # sim_data_feed.init_data(marlin_data.simulation_data, marlin_data.simulation_index)
    
    # for data_inst in sim_data_feed:
    #     marlin_data.derived_data.build_derived_data(data_inst)
    
    
    # for data_inst in sim_data_feed:
       
    #     # xr with labelled data
    #     xr = marlin_data.derived_data.query_label(time_start=data_inst.start_time, time_end=data_inst.end_time)
    #     print (xr)
    
    simulation_data_path = "/home/vixen/rs/data/acoustic/ellen/raw_repo/hp/sim"
    signature_data_path = "/home/vixen/rs/data/acoustic/ellen/raw_repo/hp/sig"

    marlin_data.load_from_path(load_args={'load_path' :simulation_data_path, "snapshot_type":"simulation", 'limit':2})
    # data = marlin_data.init_multithread(1, load_args={'location':['clyde_surfer_1']})
    # print (data.mt_snapshot_ids[0])
    
    # sim_data_feed = MarlinDataStreamer()

    # initialise data feed
    # sim_data_feed.init_data(marlin_data.simulation_data, marlin_data.simulation_index)
    # file_number_limit = 1000
    # location = ['clyde_surfer_1']

    # for snapshot in sim_data_feed:
    #     print (snapshot.meta_data)
    # for thread_id in range(0,data.number_threads):
    #     marlin_data.download_simulation_snapshots(load_args={'simulation_path':simulation_data_path, 'limit' : file_number_limit, 'location':location, 'ss_id' : data.mt_snapshot_ids[thread_id]})


  
  
    
   