from abc import ABC as _ABC
from io import BytesIO as _BytesIO
from typing import (
    Dict as _Dict, Iterable as _Iterable, List as _List, Protocol as _Protocol, 
    Tuple as _Tuple, TypeVar as _TypeVar, Union as _Union, Iterator as _Iterator
    )
from urllib.parse import urlparse as _urlparse
import numpy as _np

from pathlib import Path as _Path
from .data_utils import Prefix as _Prefix
import os as _os
import pandas as _pd
import requests as _requests

import tifffile as _tifffile #type: ignore
from PIL import Image as _Image, TiffImagePlugin as _TiffImagePlugin
_Image.MAX_IMAGE_PIXELS = None #type: ignore

from ._utils import get_minio_client as _get_minio_client
from ._config import Config as _Config #type: ignore


# Need to include rpy stubs
try: 
    import rpy2 as _rpy2 
    from rpy2 import robjects as _ro
    _RPY2_AVAILABLE = True
except:
    _RPY2_AVAILABLE = False

# If this is true then all files are written to disk locally, 
# if it is false it assumes the DPS is working with-in the CdB Framework and therefore 
# has access to the object storage

_K = _TypeVar('_K')
_V = _TypeVar('_V')
_Type = _TypeVar('_Type')

# Data Structures Mixin
class _HashMapMixin(_Protocol[_K,_V]):
    data: _Dict[_K,_V]
    
    def __getitem__(self,key: _K) -> _V:
        return self.data[key]
    
    def __setitem__(self, key: _K, value: _V) -> None:
        self.data[key] = value
        
    def __delitem__(self, key: _K) -> None:
        del self.data[key]
        
    def __contains__(self,key: _K) -> bool:
        return key in self.data
    
    def __len__(self) -> int:
        return len(self.data)
    
    def keys(self) -> _List[_K]:
        return list(self.data.keys())
    
    def values(self) -> _List[_V]:
        return list(self.data.values())
    
    def items(self) -> _List[_Tuple[_K,_V]]:
        return list(self.data.items())
    
    def clear(self) -> None:
        self.data.clear()
        
    def copy(self) -> "_HashMapMixin":
        new_dict = self.__class__()
        new_dict.data = self.data.copy()
        return new_dict
    
    def update(self, other_dict: "_HashMapMixin[_K,_V]") -> None:
        self.data.update(other_dict.data)
        
    def __str__(self) -> str:
        return str(self.data)
    
    def __repr__(self) -> str:
        return repr(self.data)
    
class _ListMixin(_Iterable,_Protocol[_V]):
    data: _List[_V]
    def __len__(self) -> int:
        return len(self.data)

    def __getitem__(self, index) -> _V:
        return self.data[index]

    def __setitem__(self, index, value: _V):
        self.data[index] = value

    def __delitem__(self, index):
        del self.data[index]

    def append(self, value: _V):
        self.data.append(value)

    def extend(self, iterable: _Iterable[_V]):
        self.data.extend(iterable)

    def insert(self, index, value: _V):
        self.data.insert(index, value)

    def remove(self, value: _V):
        self.data.remove(value)

    def pop(self, index=-1) -> _V:
        return self.data.pop(index)

    def index(self, value: _V) -> int:
        return self.data.index(value)

    def count(self, value: _V) -> int:
        return self.data.count(value)

    def sort(self):
        self.data.sort()

    def reverse(self):
        self.data.reverse()

    def __iter__(self) -> _Iterator[_V]:
        return iter(self.data)



class _StringMixin:
    def append(self, text):
        # Custom method to append text to the string
        return self.__class__(self + text)

    def reverse(self):
        # Custom method to reverse the string
        return self.__class__(self[::-1])
    
   
class _TuplePairMixin(_Protocol):
    # Doesn't do anyting - just to show that any class which is implemented as a Tuple
        # Perhaps could write a validation method which counts the number of variables implemented in the class?
    pass

       
# Syntactic Data Types and interfaces for with data storage

class _SyntacticData(_ABC):
    def __init__(self) -> None:
        super().__init__()
        
class _FilePointerMixin(_SyntacticData):
    def __init__(self) -> None:
        super().__init__()

# Need to a better way for handling write, so that it's easy to conform to the prefix convention
class _SinglePageTiff(_SyntacticData):
    """
        Mixin Class that functions as an interface which facilitates all Semantic Data Wrappers around a single page TIFF to r/w the TIFF file
        from the file system (local tool development) or the object storage (production)
    """
    # Contains information about Valid file extensions / etc..
    FILE_EXTENSION='.ome.tiff'
    # url: str 
    def __init__(self,url:str) -> None:
        self.url: str = url
        super().__init__()

    # will alway return the symbolink link to what stores the data
    @classmethod
    def write(cls, img: _Union[_Image.Image,_TiffImagePlugin.TiffImageFile], image_name: str, prefix: _Prefix):
        
        if _Config.DEBUG():
            # get cwd for python script
            base_path = _Path("./")
            prefix_path = _Path(prefix[1:]+image_name+cls.FILE_EXTENSION)
            try:
                _os.makedirs(base_path / prefix[1:])
            except FileExistsError as e:
                # This will be thrown if the directory already exists
                ...
            except OSError as e:
                print(base_path)
                print(prefix)
                raise e
                

            _tifffile.imwrite(base_path / prefix_path,_np.array(img),compression='zlib')
            url =  str((base_path / prefix_path).as_posix())

        else:
            # create buffer
            b_out = _BytesIO()
            # write to buffer
            _tifffile.imwrite(b_out,_np.array(img),compression='zlib')
            # get bytes from buffer
            b_upload = _BytesIO(b_out.getvalue())
            
            # temporary
            bucket_name =_Config._MINIO_WORKFLOW_BUCKET
            NUM_PARALLEL_UPLOADS= ''
            
            client = _get_minio_client()
            client.put_object(
                bucket_name=bucket_name, #perhaps use an environment variable?
                object_name=prefix+image_name+cls.FILE_EXTENSION, #filename + sudopath 'x/core/filename.ome.tiff'
                data=b_upload,
                num_parallel_uploads=NUM_PARALLEL_UPLOADS, #ENV Variable for setting the number of parallel uploads MINIO can use
                length=b_upload.getbuffer().nbytes
            )
            
            del b_out, b_upload
            
            url = client.get_presigned_url('GET',bucket_name,prefix+image_name+cls.FILE_EXTENSION)
        
        instance = cls(url=url)
        
        if isinstance(instance,cls):
            return instance
        else:
            raise TypeError("Write did not return an instance of the correct type.")
        
            
    def read(self) -> _Union[_Image.Image, _TiffImagePlugin.TiffImageFile]:
        if _Config.DEBUG():
            return _Image.open(self.url)
        else:
            response = _requests.get(self.url)
            return _Image.open(_BytesIO(response.content))
        
        
class _CSV(_SyntacticData):
     # Contains information about Valid file extensions / etc..
    FILE_EXTENSION='.csv'
    # url: str 
    def __init__(self,url:str) -> None:
        self.url: str = url
        super().__init__()

    @classmethod
    def write(cls, df: _pd.DataFrame, prefix: _Prefix, filename: str):
        if _Config.DEBUG():
            # get cwd for python script
            base_path = _Path("./")
            prefix_path = _Path(prefix[1:]+filename+cls.FILE_EXTENSION)
            try:
                _os.makedirs(base_path / prefix[1:])
            except FileExistsError as e:
                # This will be thrown if the directory already exists
                ...
            df.to_csv(base_path / prefix_path,index=False)
            url =  str((base_path / prefix_path).as_posix())
        else:
            # create buffer
            b_out = _BytesIO()
            # write to buffer
            df.to_csv(b_out)
            # get bytes from buffer - from here down could be abstracted
            b_upload = _BytesIO(b_out.getvalue())

            # temporary - 
            bucket_name = _Config._MINIO_WORKFLOW_BUCKET
            NUM_PARALLEL_UPLOADS= ''
            
            client = _get_minio_client()
            client.put_object(
                bucket_name=bucket_name, #perhaps use an environment variable?
                object_name=prefix+filename+cls.FILE_EXTENSION, #filename + sudopath 'x/core/filename.ome.tiff'
                data=b_upload,
                num_parallel_uploads=NUM_PARALLEL_UPLOADS, #ENV Variable for setting the number of parallel uploads MINIO can use
                length=b_upload.getbuffer().nbytes
            )
            
            del b_out, b_upload
            
            url = client.get_presigned_url('GET',bucket_name,prefix+filename+cls.FILE_EXTENSION)
        
        instance = cls(url=url)
        
        if isinstance(instance,cls):
            return instance
        else:
            raise TypeError("Write did not return an instance of the correct type.")


    def read(self) -> _pd.DataFrame:
        if _Config.DEBUG():
            return _pd.read_csv(self.url)
        else:
            response = _requests.get(self.url)
            return _pd.read_csv(_BytesIO(response.content))
    
    
    if _RPY2_AVAILABLE:
        def read_r(self) -> _ro.vectors.DataFrame:
            # wrapper for read which converts pandas df to R df
            return _ro.pandas2ri.coverter.py2rpy(self.read())

        @classmethod
        def write_r(cls,df: _ro.vectors.DataFrame, prefix: _Prefix, filename: str):
            # wrapper for wrote which converts R df to pandas df
            return cls.write(
                df= _ro.pandas2ri.coverter.rpy2py(df),
                prefix=prefix,
                filename=filename
            )
        
        
class _PNG(_SyntacticData):
    FILE_EXTENSION = ".png"
     # Contains information about Valid file extensions / etc..\
    def __init__(self,url:str) -> None:
        self.url: str = url
        super().__init__()

    # will alway return the symbolink link to what stores the data
    @classmethod
    def write(cls, img: _Union[_Image.Image,_TiffImagePlugin.TiffImageFile], image_name: str, prefix: _Prefix):

        if _Config.DEBUG():
            # get cwd for python script
            base_path = _Path(_os.getcwd())
            prefix_path = _Path(prefix+image_name+cls.FILE_EXTENSION)
            try:
                _os.makedirs(base_path / prefix)
            except FileExistsError as e:
                # This will be thrown if the directory already exists
                ...
            
            # Method for actually writing the image
            img.save(base_path / prefix_path,'PNG')
            # _tifffile.imwrite(base_path / prefix_path,np.array(img),compression='zlib')
            url =  str((base_path / prefix_path).as_posix())

        else:
            # create buffer
            b_out = _BytesIO()
            # write to buffer
            # Method for actually writing the image
            img.save(b_out,'PNG')
            # _tifffile.imwrite(b_out,np.array(img),compression='zlib')
            # get bytes from buffer
            b_upload = _BytesIO(b_out.getvalue())
            
            # temporary
            bucket_name =_Config._MINIO_WORKFLOW_BUCKET
            NUM_PARALLEL_UPLOADS= ''
            
            client = _get_minio_client()
            client.put_object(
                bucket_name=bucket_name, #perhaps use an environment variable?
                object_name=prefix+image_name+cls.FILE_EXTENSION, #filename + sudopath 'x/core/filename.ome.tiff'
                data=b_upload,
                num_parallel_uploads=NUM_PARALLEL_UPLOADS, #ENV Variable for setting the number of parallel uploads MINIO can use
                length=b_upload.getbuffer().nbytes
            )
            
            del b_out, b_upload
            
            url = client.get_presigned_url('GET',bucket_name,prefix+image_name+cls.FILE_EXTENSION)
        
        instance = cls(url=url)
        
        if isinstance(instance,cls):
            return instance
        else:
            raise TypeError("Write did not return an instance of the correct type.")
        
            
    def read(self) -> _Union[_Image.Image, _TiffImagePlugin.TiffImageFile]:
        if _Config.DEBUG():
            return _Image.open(self.url)
        else:
            response = _requests.get(self.url)
            return _Image.open(_BytesIO(response.content))
        
    def get_external_url(self) -> str:
        target = _os.environ.get('REVERSE-PROXY-HOST')
        port = _os.environ.get('REVERSE-PROXY-PORT')
        parsed_url = _urlparse(self.url)
        return parsed_url._replace(netloc=f"{target}:{port}").geturl()


# Semantic Data Types

class _SemanticData(_ABC):
    def __init__(self) -> None:
        super().__init__()
        
        # overridden methods for displaying the objects variables as strings
    def __str__(self) -> str:
        return str({name: value for name,value in self.__dict__.items() if not callable(value) and not name.startswith("__")})
    
    def __repr__(self) -> str:
        return repr({name: value for name,value in self.__dict__.items() if not callable(value) and not name.startswith("__")})


# Returns a collection (i.e. an iterable) 
class _NonAtomic(_SemanticData):
    def __init__(self) -> None:
        super().__init__()

    # Need to figure out how to enforce them implementation of decode and encode in subtypes
    # @abstractmethod
    # def encode() -> Any:
    #     ...

    # @abstractmethod
    # def decode(data: Any):
    #     ...

# Has to return a data type that isn't a wrapper, i.e. a file
class _Atomic(_SemanticData):
    def __init__(self) -> None:
        super().__init__()
    
    # Need to figure out how to enforce them implementation of decode and encode in subtypes
    # @abstractmethod
    # def encode(cls) -> Any:
    #     pass

    # @abstractmethod
    # def decode(data: Any):
    #     pass
        


######################################################
################## Cellmaps         ##################
################## Data             ##################
################## Models           ##################
##################                  ##################
######################################################
        
class TissueMicroArrayProteinChannel(_SinglePageTiff,_Atomic):
    url: str
    def __init__(self,url) -> None:
        super().__init__(url)

    @classmethod
    def decode(cls, data) -> "TissueMicroArrayProteinChannel":
        instance = cls(url=data['url'])
        return instance
    
    def encode(self) -> dict:
        return self.__dict__
    
    
    
    
class TissueMicroArray(_HashMapMixin[str,TissueMicroArrayProteinChannel],_NonAtomic):
    data: _Dict[str, TissueMicroArrayProteinChannel]
    def __init__(self) -> None:
        self.data = {}

    @classmethod
    def decode(cls, data) -> "TissueMicroArray":
        instance = cls()
        for k,v in data.items():
            instance.data[k] = TissueMicroArrayProteinChannel.decode(v)
        return instance
    
    def encode(self) -> dict:
        temp : dict = {}
        for k,v in self.data.items():
            temp[k] = v.encode()
        return temp

# Whole Slide Image
class WholeSlideImageProteinChannel(_SinglePageTiff,_Atomic):
    url: str
    def __init__(self,url) -> None:
        super().__init__(url)

    # @classmethod
    # def write(cls, img: Union[Image.Image, TiffImagePlugin.TiffImageFile], prefix: str):
    #     # system-prefix
    #     # protein-channel name
    #     return super().write(img, prefix)

    @classmethod
    def decode(cls, data) -> "WholeSlideImageProteinChannel":
        instance = cls(url=data['url'])
        return instance
    
    def encode(self) -> dict:
        return self.__dict__
    

class WholeSlideImage(_HashMapMixin[str,WholeSlideImageProteinChannel],_NonAtomic):
    data: _Dict[str, WholeSlideImageProteinChannel]
    def __init__(self) -> None:
        self.data = {}

    @classmethod
    def decode(cls, data) -> "WholeSlideImage":
        instance = cls()
        for k,v in data.items():
            instance.data[k] = WholeSlideImageProteinChannel.decode(v)
        return instance
    
    def encode(self) -> dict:
        temp : dict = {}
        for k,v in self.data.items():
            temp[k] = v.encode()
        return temp


class WholeSlideImageNucleusSegmentationMask(_SinglePageTiff,_Atomic):
    url: str
    def __init__(self,url) -> None:
        super().__init__(url)

    @classmethod
    def decode(cls, data) -> "WholeSlideImageNucleusSegmentationMask":
        instance = cls(url=data['url'])
        return instance
    
    def encode(self) -> dict:
        return self.__dict__

class WholeSlideImageMembraneSegmentationMask(_SinglePageTiff,_Atomic):
    url: str
    def __init__(self,url) -> None:
        super().__init__(url)

    @classmethod
    def decode(cls, data) -> "WholeSlideImageMembraneSegmentationMask":
        instance = cls(url=data['url'])
        return instance
    
    def encode(self) -> dict:
        return self.__dict__
        
        
class WholeSlideImageCellSegmentationMask(_NonAtomic):
    nucleus_mask: WholeSlideImageNucleusSegmentationMask
    membrane_mask: WholeSlideImageMembraneSegmentationMask

    def __init__(self, nucleus_mask: WholeSlideImageNucleusSegmentationMask, membrane_mask: WholeSlideImageMembraneSegmentationMask) -> None:
        self.nucleus_mask = nucleus_mask
        self.membrane_mask = membrane_mask

    @classmethod
    def decode(cls, data) -> "WholeSlideImageCellSegmentationMask":
        instance = cls(
            nucleus_mask = WholeSlideImageNucleusSegmentationMask.decode(data['nucleus_mask']),
            membrane_mask = WholeSlideImageMembraneSegmentationMask.decode(data['membrane_mask'])
        )
        return instance
    
    def encode(self) -> dict:
        temp: dict = {
            'nucleus_mask' : self.nucleus_mask.encode(),
            'membrane_mask' : self.membrane_mask.encode(),

        }
        return temp


# Tissue Core
class TissueCoreNucleusSegmentationMask(_SinglePageTiff,_Atomic):
    url: str
    def __init__(self,url) -> None:
        super().__init__(url)

    @classmethod
    def decode(cls, data) -> "TissueCoreNucleusSegmentationMask":
        instance = cls(url=data['url'])
        return instance
    
    def encode(self) -> dict:
        return self.__dict__
    
    # @classmethod
    # def write(cls, img: Union[Image.Image, TiffImagePlugin.TiffImageFile], image_name: str, core_name: str,  prefix: Prefix):
        
    #     return super().write(img, image_name, Prefix(prefix + f"{core_name}/"))

class TissueCoreMembraneSegmentationMask(_SinglePageTiff,_Atomic):
    url: str
    def __init__(self,url) -> None:
        super().__init__(url)

    @classmethod
    def decode(cls, data) -> "TissueCoreMembraneSegmentationMask":
        instance = cls(url=data['url'])
        return instance
    
    def encode(self) -> dict:
        return self.__dict__
    
    # @classmethod
    # def write(cls, img: Union[Image.Image, TiffImagePlugin.TiffImageFile], image_name: str, core_name: str,  prefix: Prefix):
        
    #     return super().write(img, image_name, Prefix(prefix + f"{core_name}/"))
        
        
class TissueCoreProteinChannel(_SinglePageTiff,_Atomic):
    url: str
    def __init__(self,url) -> None:
        super().__init__(url)

    @classmethod
    def decode(cls, data) -> "TissueCoreProteinChannel":
        instance = cls(url=data['url'])
        return instance
    
    def encode(self) -> dict:
        return self.__dict__
    
    # @classmethod
    # def write(cls, img: Union[Image.Image, TiffImagePlugin.TiffImageFile], image_name: str, core_name: str,  prefix: Prefix):
        
    #     return super().write(img, image_name, Prefix(prefix + f"{core_name}/"))


class TissueCore(_HashMapMixin[str,TissueCoreProteinChannel],_NonAtomic):
    data: _Dict[str, TissueCoreProteinChannel]
    def __init__(self) -> None:
        self.data = {}

    @classmethod
    def decode(cls, data) -> "TissueCore":
        instance = cls()
        for k,v in data.items():
            instance.data[k] = TissueCoreProteinChannel.decode(v)
        return instance
    
    def encode(self) -> dict:
        temp : dict = {}
        for k,v in self.data.items():
            temp[k] = v.encode()
        return temp

# To be implemented as a tuple
class TissueCoreCellSegmentationMask(_NonAtomic):
    nucleus_mask: TissueCoreNucleusSegmentationMask
    membrane_mask: TissueCoreMembraneSegmentationMask

    def __init__(self, nucleus_mask: TissueCoreNucleusSegmentationMask, membrane_mask: TissueCoreMembraneSegmentationMask) -> None:
        self.nucleus_mask = nucleus_mask
        self.membrane_mask = membrane_mask

    @classmethod
    def decode(cls, data) -> "TissueCoreCellSegmentationMask":
        # instance = cls(url=data['url'])
        instance = cls(
            nucleus_mask = TissueCoreNucleusSegmentationMask.decode(data['nucleus_mask']),
            membrane_mask = TissueCoreMembraneSegmentationMask.decode(data['membrane_mask'])
        )
        return instance
    
    def encode(self) -> dict:
        temp: dict = {
            'nucleus_mask' : self.nucleus_mask.encode(),
            'membrane_mask' : self.membrane_mask.encode(),

        }
        return temp
    

# DearrayedTissueMicroArray
class DearrayedTissueMicroArrayCellSegmentationMask(_HashMapMixin[str,TissueCoreCellSegmentationMask],_NonAtomic):
    data: _Dict[str,TissueCoreCellSegmentationMask]
    def __init__(self) -> None:
        self.data = {}

    @classmethod
    def decode(cls, data) -> "DearrayedTissueMicroArrayCellSegmentationMask":
        instance = cls()
        for k,v in data.items():
            instance.data[k] = TissueCoreCellSegmentationMask.decode(v)
        return instance
    
    def encode(self) -> dict:
        temp: dict = {}
        for k,v in self.data.items():
            temp[k] = v.encode()
        return temp
    


class DearrayedTissueMicroArray(_HashMapMixin[str,TissueCore],_NonAtomic):
    data: _Dict[str, TissueCore]
    def __init__(self) -> None:
        self.data= {}

    @classmethod
    def decode(cls, data) -> "DearrayedTissueMicroArray":
        instance = cls()
        for k,v in data.items():
            instance.data[k] = TissueCore.decode(v)
        return instance
    
    def encode(self) -> dict:
        temp: dict = {}
        for k,v in self.data.items():
            temp[k] = v.encode()
        return temp


class WholeSlideImageMissileFCS(_CSV,_Atomic):
    # Enforce these as 
    _SCHEMA = {
        "Cell_ID":  int,
        "Region": int, 
        "x": int, 
        "y": int,
        "Size": int,
        "Perimeter": float,
        "MajorAxisLength": float,
        "MinorAxisLength": float,
        "Eccentricity": float,
        "Solidity": float,
        "MajorMinorAxisRatio": float,
        "PerimeterSquareToArea": float,
        "MajorAxisToEquivalentDiam": float,
        "NucCytoRatio": float,
        "*" : float #wildcard to match all other columns
    }


    url: str
    def __init__(self,url) -> None:
        super().__init__(url)
    
    @classmethod
    def decode(cls, data) -> "WholeSlideImageMissileFCS":
        instance = cls(url=data['url'])
        return instance
    
    def encode(self) -> dict:
        # Need to ignore _REQUIRED_COLUMN_NAMES
        return {k: v for k, v in self.__dict__.items() if k[0] != "_"}

# To be implemented;
    
class TissueCoreMissileFCS(_CSV,_Atomic):
    _SCHEMA = {
        "Cell_ID":  int,
        "Region": int, 
        "x": int, 
        "y": int,
        "Size": int,
        "Perimeter": float,
        "MajorAxisLength": float,
        "MinorAxisLength": float,
        "Eccentricity": float,
        "Solidity": float,
        "MajorMinorAxisRatio": float,
        "PerimeterSquareToArea": float,
        "MajorAxisToEquivalentDiam": float,
        "NucCytoRatio": float,
        "*" : float #wildcard to match all other columns
    }

    url: str
    def __init__(self,url) -> None:
        super().__init__(url)
    
    @classmethod
    def decode(cls, data) -> "TissueCoreMissileFCS":
        instance = cls(url=data['url'])
        return instance
    
    def encode(self) -> dict:
        # Need to ignore _REQUIRED_COLUMN_NAMES
        return {k: v for k, v in self.__dict__.items() if k[0] != "_"}
    
# -> This FCS is specifically designed to work with Missile;
class DearrayedTissueMicroArrayMissileFCS(_HashMapMixin[str,TissueCoreMissileFCS],_NonAtomic):
    data: _Dict[str, TissueCoreMissileFCS]
    def __init__(self) -> None:
        self.data = {}

    @classmethod
    def decode(cls, data) -> "DearrayedTissueMicroArrayMissileFCS":
        instance = cls()
        for k,v in data.items():
            instance.data[k] = TissueCoreMissileFCS.decode(v)
        return instance
    
    def encode(self) -> dict:
        temp : dict = {}
        for k,v in self.data.items():
            temp[k] = v.encode()
        return temp
    

class Plot(_PNG,_Atomic):
    url: str
    def __init__(self,url) -> None:
        super().__init__(url)

    @classmethod
    def decode(cls, data) -> "Plot":
        instance = cls(url=data['url'])
        return instance
    
    def encode(self) -> dict:
        return self.__dict__

# Workflow Parameters
class NuclearStain(str, _StringMixin,_Atomic):
    """
        This is a Semantic Wrapper for a string which denotes it as being a Nuclear Stain;
    """
    def __init__(self, value) -> None:
        ...

    def __new__(cls, value):
        return super().__new__(cls, value)
    
    @classmethod
    def decode(cls, data) -> "NuclearStain":
        return cls(data)
    
    def encode(self) -> str:
        return str(self)
    
   
    
class NuclearMarker(str,_StringMixin,_Atomic):
    
    def __init__(self, value) -> None:
        ...

    def __new__(cls, value):
        return super().__new__(cls, value)
    
    @classmethod
    def decode(cls, data) -> "NuclearMarker":
        return cls(data)
    
    def encode(self) -> str:
        return self
    

class NuclearMarkers(_ListMixin[NuclearMarker],_NonAtomic):
    """
        This is a Semantic Wrapper for a list of NuclearMarker;
    """
    data: _List[NuclearMarker]

    def __init__(self) -> None:
        self.data= []

    @classmethod
    def decode(cls, data) -> "NuclearMarkers":
        instance = cls()
        for v in data:
            instance.data.append(NuclearMarker.decode(v))

        return instance
    
    def encode(self) -> _List:
        
        return self.data
    
class MembraneMarker(str,_StringMixin,_Atomic):
    """
        This is a Semantic Wrapper for a string which denotes it as being a Membrane Marker;
    """
    def __init__(self, value) -> None:
        ...

    def __new__(cls, value):
        return super().__new__(cls, value)
    
    @classmethod
    def decode(cls, data) -> "MembraneMarker":
        return cls(data)
    
    def encode(self) -> str:
        return str(self)
    
class MembraneMarkers(_ListMixin[MembraneMarker],_NonAtomic):
    """
        This is a Semantic Wrapper for a list of MembraneMarker;
    """
    data: _List[MembraneMarker]

    def __init__(self) -> None:
        self.data= []

    @classmethod
    def decode(cls, data) -> "MembraneMarkers":
        instance = cls()
        for v in data:
            instance.data.append(MembraneMarker.decode(v))

        return instance
    
    def encode(self) -> _List:
        
        return [v.encode() for v in self.data]
    
class ProteinChannelMarker(str,_StringMixin,_Atomic):
    def __init__(self, value) -> None:
        ...

    def __new__(cls, value):
        return super().__new__(cls, value)
    
    @classmethod
    def decode(cls, data) -> "ProteinChannelMarker":
        return cls(data)
    
    def encode(self) -> str:
        return str(self)

class ProteinChannelMarkers(_ListMixin[ProteinChannelMarker],_NonAtomic):
    """
        This is a Semantic Wrapper for a list of MembraneMarker;
    """
    data: _List[ProteinChannelMarker]

    def __init__(self) -> None:
        self.data= []

    @classmethod
    def decode(cls, data) -> "ProteinChannelMarkers":
        instance = cls()
        for v in data:
            instance.data.append(ProteinChannelMarker.decode(v))

        return instance
    
    def encode(self) -> _List:
        return [v.encode() for v in self.data]

class ROI(_Atomic):
    x1: float
    y1: float
    x2: float
    y2: float
    img_w: float
    img_h: float
    def __init__(self,x1,y1,x2,y2,img_w,img_h) -> None:
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.img_w = img_w
        self.img_h = img_h
        # super().__init__(url)

    @classmethod
    def decode(cls, data) -> "ROI":
        instance = cls(
            x1 = data["x1"],
            y1 = data["y1"],
            x2 = data["x2"],
            y2 = data["y2"],
            img_w = data["img_w"],
            img_h = data["img_h"],
        )
        return instance
    
    def encode(self) -> dict:
        return self.__dict__
    

class ROIs(_ListMixin[ROI],_NonAtomic):
    """
        This is a Semantic Wrapper for a list of ROI's;
    """
    data: _List[ROI]

    def __init__(self) -> None:
        self.data= []


    @classmethod
    def decode(cls, data) -> "ROIs":
        instance = cls()
        for v in data:
            instance.data.append(ROI.decode(v))

        return instance
    
    # If the atomic type only contains k,v pairs like a dict encode in higher level class returns a dict
        # Perhaps a nicer solution for this would be useful
    def encode(self) -> _List[dict]:
        temp = []
        for v in self.data:
            temp.append(v.encode())
        
        return temp
    

class ROIsPredictionWrapper(_NonAtomic):
    confidence_value: float
    rois: ROIs

    def __init__(self, confidence_value, rois) -> None:
        self.confidence_value = confidence_value
        self.rois = rois

    @classmethod
    def decode(cls, data) -> "ROIsPredictionWrapper":
        instance = cls(
            confidence_value=data['confidence_value'],
            rois=ROIs.decode(data['rois'])
        )
        

        return instance
    
    # If the atomic type only contains k,v pairs like a dict encode in higher level class returns a dict
        # Perhaps a nicer solution for this would be useful
    def encode(self) -> dict:
        temp = {
            "confidence_value": self.confidence_value,
            "rois": self.rois.encode()
        }
        
        return temp
    

class PredictedROIs(_ListMixin[ROIsPredictionWrapper],_NonAtomic):
    """
        This is a Semantic Wrapper for a list of ROIsPredictionWrapper (which is itself a semantic wrapper for a list of predicted ROIs and the confidence value used as a gate for the segmentation model);
    """
    data: _List[ROIsPredictionWrapper]

    def __init__(self) -> None:
        self.data= []

    @classmethod
    def decode(cls, data) -> "PredictedROIs":
        instance = cls()
        for v in data:
            instance.data.append(ROIsPredictionWrapper.decode(v))

        return instance
    
    # If the atomic type only contains k,v pairs like a dict encode in higher level class returns a dict
        # Perhaps a nicer solution for this would be useful
    def encode(self) -> _List[dict]:
        temp = []
        for v in self.data:
            temp.append(v.encode())
        
        return temp
    
# Only include if Rpy2  is installed (or add functionality if r is installed)

# Missile Data Types

class MissileExpressionCounts(_CSV, _Atomic):
    # Columns are the protein channel names
    _SCHEMA : _Dict[str,_Type] = {
        "*" : float #wildcard to match all other columns
    }
    url: str

    def __init__(self,url) -> None:
        super().__init__(url)
    
    @classmethod
    def decode(cls, data) -> "MissileExpressionCounts":
        instance = cls(url=data['url'])
        return instance
    
    def encode(self) -> dict:
        # Need to ignore_REQUIRED_COLUMN_NAMES
        return self.__dict__
    
class MissileExpressionSpatialData(_CSV, _Atomic):
    # Enforce these as 
    # Columns are the protein channel names
    _SCHEMA : _Dict[str,_Type] = {
        "x": int, 
        "y": int,
    }
    url: str

    def __init__(self,url) -> None:
        super().__init__(url)
    
    @classmethod
    def decode(cls, data) -> "MissileExpressionSpatialData":
        instance = cls(url=data['url'])
        return instance
    
    def encode(self) -> dict:
        # Need to ignore_REQUIRED_COLUMN_NAMES
        return {k: v for k, v in self.__dict__.items() if k[0] != "_"}
    
    

class MissileMetadata(_CSV, _Atomic):
    # Columns are the metadata (i.e. the features)
    _SCHEMA : _Dict[str,_Type] = {
        "allRegions": int, 
        "Size": int,
        "Perimeter": float,
        "MajorAxisLength": float,
        "MinorAxisLength": float,
        "Eccentricity": float,
        "Solidity": float,
        "MajorMinorAxisRatio": float,
        "PerimeterSquareToArea": float,
        "MajorAxisToEquivalentDiam": float,
        "NucCytoRatio": float
    }
    url: str
    def __init__(self,url) -> None:
        super().__init__(url)
    
    @classmethod
    def decode(cls, data) -> "MissileMetadata":
        instance = cls(url=data['url'])
        return instance
    
    def encode(self) -> dict:
        # Need to ignore_REQUIRED_COLUMN_NAMES
        return {k:v for k,v in self.__dict__.items() if k[0] != "_"}
    
    


# cluster_labels
class MissileClusters(_CSV,_Atomic):
     # Enforce these as 
    # Columns are the protein channel names
    _SCHEMA : _Dict[str,_Type] = {"cluster_labels": int}
    url: str

    def __init__(self,url) -> None:
        super().__init__(url)
    
    @classmethod
    def decode(cls, data) -> "MissileClusters":
        instance = cls(url=data['url'])
        return instance
    
    def encode(self) -> dict:
        # Need to ignore_REQUIRED_COLUMN_NAMES
        return {k: v for k, v in self.__dict__.items() if k[0] != "_"}
    


# Neighbourhood Labels
class MissileNeighbourhoods(_CSV,_Atomic):
     # Enforce these as 
    # Columns are the protein channel names
    _SCHEMA : _Dict[str,_Type] = {"cluster_labels": int}
    url: str

    def __init__(self,url) -> None:
        super().__init__(url)
    
    @classmethod
    def decode(cls, data) -> "MissileClusters":
        instance = cls(url=data['url'])
        return instance
    
    def encode(self) -> dict:
        # Need to ignore_REQUIRED_COLUMN_NAMES
        return {k: v for k, v in self.__dict__.items() if k[0] != "_"}