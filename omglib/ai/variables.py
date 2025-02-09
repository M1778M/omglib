from ..tools.dicttools import perfectdict
from pathlib import Path
import random as _random
from pySmartDL import SmartDL as _download
from zipfile import ZipFile as _ZipFile
import shutil as _shutil
from whisper import available_models as _wa

class Languages:
    English='en';French='fr';Spanish='es';Mandarin='zh';Hindi='hi';Arabic='ar';Bengali='bn';Portuguese='pt';Russian='ru';Japanese='ja';Punjabi='pa';German='de';Korean='ko';Vietnamese='vi';Turkish='tr';Italian='it';Tamil='ta';Urdu='ur';Persian='fa';Dutch='nl';Thai='th';Malay='ms';Swahili='sw';Greek='el';Hungarian='hu';Polish='pl';Ukrainian='uk';Hebrew='he';Finnish='fi';Danish='da';Czech='cs';Slovak='sk';Norwegian='no';Swedish='sv';Romanian='ro';Bulgarian='bg';Croatian='hr';Serbian='sr';Slovenian='sl';Estonian='et';Latvian='lv';Lithuanian='lt';Icelandic='is';Irish='ga';Maltese='mt';Basque='eu';Catalan='ca';Galician='gl';Kurdish='ku';Amharic='am';Zulu='zu';Xhosa='xh';Yoruba='yo';Hausa='ha';Igbo='ig';Somali='so';Albanian='sq';Bosnian='bs';Macedonian='mk';Azerbaijani='az';Armenian='hy';Georgian='ka';Sinhala='si';Khmer='km';Lao='lo';Burmese='my';Mongolian='mn';Pashto='ps';Kazakh='kk';Uzbek='uz';Tajik='tg';Kyrgyz='ky';Turkmen='tk';Malayalam='ml';Kannada='kn';Telugu='te';Marathi='mr';Gujarati='gu';Oriya='or';Assamese='as';Nepali='ne';Tibetan='bo';Maori='mi';Samoan='sm';Tongan='to';Fijian='fj';Malagasy='mg';Sesotho='st';Tswana='tn';Shona='sn';Afrikaans='af';Lingala='ln';Luo='luo';Kinyarwanda='rw';Kirundi='rn';Quechua='qu';Aymara='ay';Guarani='gn';Nahuatl='nah'


Path().home().joinpath(".omgl/").joinpath("vosk_models/").mkdir(parents=True,exist_ok=True)

class VoskModelSize:
    Small = 'small'
    Medium = 'medium'
    Large = 'large'

class VoskModels:
    supported_languages = { # The data may not be accurate
    'en':{'small':{'name':'vosk-model-small-en-us-0.15','link':'https://alphacephei.com/vosk/models/vosk-model-small-en-us-0.15.zip'},'medium':{'name':'vosk-model-en-us-0.22','link':'https://alphacephei.com/vosk/models/vosk-model-en-us-0.22.zip'},'large':{'name':'vosk-model-en-us-0.42-gigaspeech','link':'https://alphacephei.com/vosk/models/vosk-model-en-us-0.42-gigaspeech.zip'}} # English
    ,'en_in':{'small':{'name':'vosk-model-small-en-in-0.4','link':'https://alphacephei.com/vosk/models/vosk-model-small-en-in-0.4.zip'},'medium':{'name':'vosk-model-en-in-0.5','link':'https://alphacephei.com/vosk/models/vosk-model-en-in-0.5.zip'}} # Indian English
    ,'cn':{'small':{'name':'vosk-model-small-cn-0.22','link':'https://alphacephei.com/vosk/models/vosk-model-small-cn-0.22.zip'},'medium':{'name':'vosk-model-cn-0.22','link':'https://alphacephei.com/vosk/models/vosk-model-cn-0.22.zip'},'large':{'name':'vosk-model-cn-kaldi-multicn-0.15','link':'https://alphacephei.com/vosk/models/vosk-model-cn-kaldi-multicn-0.15.zip'}} # Chinese
    ,'ru':{'small':{'name':'vosk-model-small-ru-0.22','link':'https://alphacephei.com/vosk/models/vosk-model-small-ru-0.22.zip'},'medium':{'name':'vosk-model-ru-0.42','link':'https://alphacephei.com/vosk/models/vosk-model-ru-0.42.zip'},'large':{'name':'vosk-model-ru-0.10','link':'https://alphacephei.com/vosk/models/vosk-model-ru-0.10.zip'}} # Russian
    ,'fr':{'small':{'name':'vosk-model-small-fr-0.22','link':'https://alphacephei.com/vosk/models/vosk-model-small-fr-0.22.zip'},'medium':{'name':'vosk-model-fr-0.22','link':'https://alphacephei.com/vosk/models/vosk-model-fr-0.22.zip'},'large':{'name':'vosk-model-fr-0.6-linto-2.2.0','link':'https://alphacephei.com/vosk/models/vosk-model-fr-0.6-linto-2.2.0.zip'}} # French
    ,'de':{'small':{'name':'vosk-model-small-de-0.15','link':'https://alphacephei.com/vosk/models/vosk-model-small-de-0.15.zip'},'medium':{'name':'vosk-model-de-0.21','link':'https://alphacephei.com/vosk/models/vosk-model-de-0.21.zip'},'large':{'name':'vosk-model-de-tuda-0.6-900k','link':'https://alphacephei.com/vosk/models/vosk-model-de-tuda-0.6-900k.zip'}} # German
    ,'es':{'small':{'name':'vosk-model-small-es-0.42','link':'https://alphacephei.com/vosk/models/vosk-model-small-es-0.42.zip'},'medium':{'name':'vosk-model-es-0.42','link':'https://alphacephei.com/vosk/models/vosk-model-es-0.42.zip'}} # Spanish
    ,'pt':{'small':{'name':'vosk-model-small-pt-0.3','link':'https://alphacephei.com/vosk/models/vosk-model-small-pt-0.3.zip'},'medium':{'name':'vosk-model-pt-fb-v0.1.1-20220516_2113','link':'https://alphacephei.com/vosk/models/vosk-model-pt-fb-v0.1.1-20220516_2113.zip'}} # Portuguese/Brazilian
    ,'gr':{'medium':{'name':'vosk-model-el-gr-0.7','link':'https://alphacephei.com/vosk/models/vosk-model-el-gr-0.7.zip'}} # Greek
    ,'tr':{'small':{'name':'vosk-model-small-tr-0.3','link':'https://alphacephei.com/vosk/models/vosk-model-small-tr-0.3.zip'}} # Turkish
    ,'vn':{'small':{'name':'vosk-model-small-vn-0.4','link':'https://alphacephei.com/vosk/models/vosk-model-small-vn-0.4.zip'},'medium':{'name':'vosk-model-vn-0.4','link':'https://alphacephei.com/vosk/models/vosk-model-vn-0.4.zip'}} # Vietnamese
    ,'it':{'small':{'name':'vosk-model-small-it-0.22','link':'https://alphacephei.com/vosk/models/vosk-model-small-it-0.22.zip'},'medium':{'name':'vosk-model-it-0.22','link':'https://alphacephei.com/vosk/models/vosk-model-it-0.22.zip'}} # Italian
    ,'nl':{'small':{'name':'vosk-model-small-nl-0.22','link':'https://alphacephei.com/vosk/models/vosk-model-small-nl-0.22.zip'},'medium':{'name':'vosk-model-nl-spraakherkenning-0.6','link':'https://alphacephei.com/vosk/models/vosk-model-nl-spraakherkenning-0.6.zip'}} # Dutch
    ,'ar':{'small':{'name':'vosk-model-ar-mgb2-0.4','link':'https://alphacephei.com/vosk/models/vosk-model-ar-mgb2-0.4.zip'},'medium':{'name':'vosk-model-ar-0.22-linto-1.1.0','link':'https://alphacephei.com/vosk/models/vosk-model-ar-0.22-linto-1.1.0.zip'}} # Arabic
    ,'fa':{'small':{'name':'vosk-model-small-fa-0.5','link':'https://alphacephei.com/vosk/models/vosk-model-small-fa-0.5.zip'},'medium':{'name':'vosk-model-fa-0.42','link':'https://alphacephei.com/vosk/models/vosk-model-fa-0.42.zip'}} # Farsi/Persian
    ,'ph':{'small':{'name':'vosk-model-tl-ph-generic-0.6','link':'https://alphacephei.com/vosk/models/vosk-model-tl-ph-generic-0.6.zip'}} # Filipino
    ,'uk':{'small':{'name':'vosk-model-small-uk-v3-small','link':'https://alphacephei.com/vosk/models/vosk-model-small-uk-v3-small.zip'},'medium':{'name':'vosk-model-uk-v3','link':'https://alphacephei.com/vosk/models/vosk-model-uk-v3.zip'}} # Ukrainian
    ,'sv':{'small':{'name':'vosk-model-small-sv-rhasspy-0.15','link':'https://alphacephei.com/vosk/models/vosk-model-small-sv-rhasspy-0.15.zip'}} # Swedish
    ,'ja':{'small':{'name':'vosk-model-small-ja-0.22','link':'https://alphacephei.com/vosk/models/vosk-model-small-ja-0.22.zip'},'medium':{'name':'vosk-model-ja-0.22','link':'https://alphacephei.com/vosk/models/vosk-model-ja-0.22.zip'}} # Japanese
    ,'hi':{'small':{'name':'vosk-model-small-hi-0.22','link':'https://alphacephei.com/vosk/models/vosk-model-small-hi-0.22.zip'},'medium':{'name':'vosk-model-hi-0.22','link':'https://alphacephei.com/vosk/models/vosk-model-hi-0.22.zip'}} # Hindi
    ,'pl':{'small':{'name':'vosk-model-small-pl-0.22','link':'https://alphacephei.com/vosk/models/vosk-model-small-pl-0.22.zip'}} # Polish
    ,'ko':{'small':{'name':'vosk-model-small-ko-0.22','link':'https://alphacephei.com/vosk/models/vosk-model-small-ko-0.22.zip'}} # Korean
    ,'tg':{'small':{'name':'vosk-model-small-tg-0.22','link':'https://alphacephei.com/vosk/models/vosk-model-small-tg-0.22.zip'},'medium':{'name':'vosk-model-tg-0.22','link':'https://alphacephei.com/vosk/models/vosk-model-tg-0.22.zip'}} # Tajik
    }
    def GetModel(language:str,size:str):
        if not perfectdict.has_key(VoskModels.supported_languages,language):
            assert VoskModels.supported_languages[language]
        model_=perfectdict.get_key(VoskModels.supported_languages[language],size)
        if model_ == None:
            return VoskModels.GetSmallerModel(language,size)
        return model_
    def AddVoskModel(name:str,language:str,link:str):
        if perfectdict.has_key(VoskModels.supported_languages,language):
            if perfectdict.has_key(VoskModels.supported_languages[language],'custom') and type(VoskModels.supported_languages[language]['custom']) == list:
                VoskModels.supported_languages[language]['custom'].append({'name':name,'link':link})
            else:
                VoskModels.supported_languages[language]['custom']=[]
                VoskModels.supported_languages[language]['custom'].append({'name':name,'link':link})
        else:
            VoskModels.supported_languages[language] = {}
            VoskModels.AddVoskModel(name,language,link)
        return True
    def GetSmallestModel(language:str):
        if not perfectdict.has_key(VoskModels.supported_languages,language):
            assert VoskModels.supported_languages[language]
        
        if perfectdict.has_key(VoskModels.supported_languages[language],'small'):
            return perfectdict.get_key(VoskModels.supported_languages[language],'small')
        elif perfectdict.has_key(VoskModels.supported_languages[language],'medium'):
            return perfectdict.get_key(VoskModels.supported_languages[language],'medium')
        elif perfectdict.has_key(VoskModels.supported_languages[language],'custom'):
            return perfectdict.get_key(VoskModels.supported_languages[language],'custom')[0]
        elif perfectdict.has_key(VoskModels.supported_languages[language],'large'):
            return perfectdict.get_key(VoskModels.supported_languages[language],'large')
        else:
            return None
    def GetBestModel(language:str):
        if not perfectdict.has_key(VoskModels.supported_languages,language):
            assert VoskModels.supported_languages[language]
        if perfectdict.has_key(VoskModels.supported_languages[language],'large'):
            return perfectdict.get_key(VoskModels.supported_languages[language],'large')
        elif perfectdict.has_key(VoskModels.supported_languages[language],'medium'):
            return perfectdict.get_key(VoskModels.supported_languages[language],'medium')
        elif perfectdict.has_key(VoskModels.supported_languages[language],'custom'):
            return perfectdict.get_key(VoskModels.supported_languages[language],'custom')[0]
        elif perfectdict.has_key(VoskModels.supported_languages[language],'small'):
            return perfectdict.get_key(VoskModels.supported_languages[language],'small')
        else:
            return None
    def GetCustomModels(language:str):
        if not perfectdict.has_key(VoskModels.supported_languages,language):
            assert VoskModels.supported_languages[language]
        if not perfectdict.has_key(VoskModels.supported_languages[language],'custom'):
            return None
        return perfectdict.get_key(VoskModels.supported_languages[language],'custom')
    def GetRandomModel(language:str):
        if not perfectdict.has_key(VoskModels.supported_languages,language):
            assert VoskModels.supported_languages[language]
        return VoskModels.supported_languages[language][_random.choice(list(VoskModels.supported_languages[language].keys()))]
    def GetMediumModel(language:str):
        if not perfectdict.has_key(VoskModels.supported_languages,language):
            assert VoskModels.supported_languages[language]
        return perfectdict.get_key(VoskModels.supported_languages[language],'medium')
    def GetSmallerModel(language:str,weight:str):
        if not perfectdict.has_key(VoskModels.supported_languages,language):
            assert VoskModels.supported_languages[language]
        if weight == 'large':
            return perfectdict.get_key(VoskModels.supported_languages[language],'medium')
        elif weight == 'medium':
            return perfectdict.get_key(VoskModels.supported_languages[language],'small')
        elif weight == 'small':
            return perfectdict.get_key(VoskModels.supported_languages[language],'small')
        else:
            assert ValueError(f"Unknown weight {weight}, unable to get smaller model.")
    def GetLargerModel(language:str,weight:str):
        if not perfectdict.has_key(VoskModels.supported_languages,language):
            assert VoskModels.supported_languages[language]
        if weight == 'small':
            return perfectdict.get_key(VoskModels.supported_languages[language],'medium')
        elif weight == 'medium':
            return perfectdict.get_key(VoskModels.supported_languages[language],'large')
        elif weight == 'large':
            return perfectdict.get_key(VoskModels.supported_languages[language],'large')
        else:
            assert ValueError(f"Unknown weight {weight}, unable to get larger model.")
    def GetAvailableSizes(language:str):
        if not perfectdict.has_key(VoskModels.supported_languages,language):
            assert VoskModels.supported_languages[language]
        return perfectdict.get_keys(VoskModels.supported_languages[language])
    def GetAvailableLangs():
        return perfectdict.get_keys(VoskModels.supported_languages)

class _VMM_CUSTOM_DOWNLOAD_MANAGER:
    def __init__(self,download_obj:_download,model:dict):
        self.obj=download_obj
        self.model = model
    def status(self): #paused, downloading, finished
        return self.obj.get_status()
    def start(self):
        self.obj.start(False)
        return True
    def restart(self,auto_start=False):
        self.obj.retry()
        self.obj.start()
        return True
    def is_finished(self):
        if self.obj.isFinished():
            return True
        return False
    def finished_and_successful(self):
        return self.obj.isFinished() and self.obj.isSuccessful()
    def string_full_status(self):
        try:
            return f"Downloading ({self.obj.get_speed(True)}) {self.obj.get_progress_bar(30)} {self.obj.get_dl_size(True)}/{self.obj.get_final_filesize(True)} {self.obj.get_eta(True)}"
        except Exception as err:
            print(f"ERROR: {err}")
            return ""
    def after_download(self):
        def _get_only_folder(folder_path:str):
            folder = Path(folder_path)

            # Ensure the path is a directory
            if not folder.exists() or not folder.is_dir():
                raise FileNotFoundError(f"The path '{folder_path}' does not exist or is not a directory.")
            
            # List all subdirectories in the given folder
            subfolders = [f for f in folder.iterdir() if f.is_dir()]
            
            # Check if exactly one folder exists
            if len(subfolders) == 0:
                raise ValueError(f"No folders found in '{folder_path}'.")
            elif len(subfolders) > 1:
                raise ValueError(f"More than one folder found in '{folder_path}': {', '.join(str(f) for f in subfolders)}")
            
            # Return the single folder
            return subfolders[0]
        
        downloaded = self.obj
        prints=False
        model=self.model
        if downloaded.isFinished():
            if prints:print("Model download completed. installing model...")
            zfile=downloaded.get_dest()
            _ZipFile(zfile).extractall(str(Path(VMM.models_path).joinpath(model['name'])))
            Path(VMM.models_path).joinpath('temp').mkdir(exist_ok=True)
            try:
                orgn=_get_only_folder(Path(VMM.models_path).joinpath(model['name'])).name
                _shutil.move(_get_only_folder(Path(VMM.models_path).joinpath(model['name'])),Path(VMM.models_path).joinpath("temp"))
                temp_folder_name= _get_only_folder(Path(VMM.models_path).joinpath('temp')).name
                _shutil.rmtree(Path(VMM.models_path).joinpath(model['name']))
                _shutil.move(_get_only_folder(Path(VMM.models_path).joinpath('temp')),Path(VMM.models_path))
                _shutil.rmtree(Path(VMM.models_path).joinpath('temp'))
                Path(VMM.models_path).joinpath(temp_folder_name).rename(Path(VMM.models_path).joinpath(model['name']))
            except Exception as err: raise SystemError(err)
            if Path(VMM.models_path).joinpath(orgn):
                if prints:print("Model successfully installed.")
                return True
            else:
                raise SystemError("System failed to install the model.")
        else:
            if prints:print("Model download failed. quiting...")
            return False
    

class VMM: # Vosk Model Manager
    models_path = str(Path().home().joinpath(".omgl/").joinpath("vosk_models/"))
    def change_models_path(newpath:str):
        VMM.models_path = str(Path(newpath).absolute())
        return True
    def get_model_path(model:dict):
        return str(Path(VMM.models_path).joinpath(model['name']))
    def smart_download(model:dict,prints:bool=False):
        def _get_only_folder(folder_path:str):
            folder = Path(folder_path)
    
            # Ensure the path is a directory
            if not folder.exists() or not folder.is_dir():
                raise FileNotFoundError(f"The path '{folder_path}' does not exist or is not a directory.")
            
            # List all subdirectories in the given folder
            subfolders = [f for f in folder.iterdir() if f.is_dir()]
            
            # Check if exactly one folder exists
            if len(subfolders) == 0:
                raise ValueError(f"No folders found in '{folder_path}'.")
            elif len(subfolders) > 1:
                raise ValueError(f"More than one folder found in '{folder_path}': {', '.join(str(f) for f in subfolders)}")
            
            # Return the single folder
            return subfolders[0]
        
        if prints:
            print("Checking to see if model is already installed...")
        if Path(VMM.models_path).joinpath(model['name']+'.zip').exists():
            zfile=str(Path(VMM.models_path).joinpath(model['name']+'.zip'))
            _ZipFile(zfile).extractall(str(Path(VMM.models_path).joinpath(model['name'])))
            Path(VMM.models_path).joinpath('temp').mkdir(exist_ok=True)
            try:
                orgf=_get_only_folder(Path(VMM.models_path).joinpath(model['name']))
                orgn=_get_only_folder(Path(VMM.models_path).joinpath(model['name'])).name
                _shutil.move(_get_only_folder(Path(VMM.models_path).joinpath(model['name'])),Path(VMM.models_path).joinpath("temp"))
                _shutil.rmtree(Path(VMM.models_path).joinpath(model['name']))
                temp_folder_name= _get_only_folder(Path(VMM.models_path).joinpath('temp')).name
                _shutil.move(_get_only_folder(Path(VMM.models_path).joinpath('temp')),Path(VMM.models_path))
                _shutil.rmtree(Path(VMM.models_path).joinpath('temp'))
                Path(VMM.models_path).joinpath(temp_folder_name).rename(Path(VMM.models_path).joinpath(model['name']))
            except Exception as err: raise SystemError(err)
            if Path(VMM.models_path).joinpath(orgn):
                if prints:print("Model successfully installed.")
                return True
            else:
                raise SystemError("System failed to install the model.")
        if Path(VMM.models_path).joinpath(model['name']).exists():
            return True
        if prints:print("model is not installed, downloading model...")
        dest=str(Path(VMM.models_path).joinpath(model['name']+'.zip'))

        downloaded=_download(model['link'],dest,False)
        return _VMM_CUSTOM_DOWNLOAD_MANAGER(downloaded,model)
        
    def install_model(model:dict,prints=False):
        def _get_only_folder(folder_path:str):
            folder = Path(folder_path)
    
            # Ensure the path is a directory
            if not folder.exists() or not folder.is_dir():
                raise FileNotFoundError(f"The path '{folder_path}' does not exist or is not a directory.")
            
            # List all subdirectories in the given folder
            subfolders = [f for f in folder.iterdir() if f.is_dir()]
            
            # Check if exactly one folder exists
            if len(subfolders) == 0:
                raise ValueError(f"No folders found in '{folder_path}'.")
            elif len(subfolders) > 1:
                raise ValueError(f"More than one folder found in '{folder_path}': {', '.join(str(f) for f in subfolders)}")
            
            # Return the single folder
            return subfolders[0]
        
        if prints:
            print("Checking to see if model is already installed...")
        if Path(VMM.models_path).joinpath(model['name']+'.zip').exists():
            zfile=str(Path(VMM.models_path).joinpath(model['name']+'.zip'))
            _ZipFile(zfile).extractall(str(Path(VMM.models_path).joinpath(model['name'])))
            Path(VMM.models_path).joinpath('temp').mkdir(exist_ok=True)
            try:
                orgf=_get_only_folder(Path(VMM.models_path).joinpath(model['name']))
                orgn=_get_only_folder(Path(VMM.models_path).joinpath(model['name'])).name
                _shutil.move(_get_only_folder(Path(VMM.models_path).joinpath(model['name'])),Path(VMM.models_path).joinpath("temp"))
                _shutil.rmtree(Path(VMM.models_path).joinpath(model['name']))
                temp_folder_name= _get_only_folder(Path(VMM.models_path).joinpath('temp')).name
                _shutil.move(_get_only_folder(Path(VMM.models_path).joinpath('temp')),Path(VMM.models_path))
                _shutil.rmtree(Path(VMM.models_path).joinpath('temp'))
                Path(VMM.models_path).joinpath(temp_folder_name).rename(Path(VMM.models_path).joinpath(model['name']))
            except Exception as err: raise SystemError(err)
            if Path(VMM.models_path).joinpath(orgn):
                if prints:print("Model successfully installed.")
                return True
            else:
                raise SystemError("System failed to install the model.")
        if Path(VMM.models_path).joinpath(model['name']).exists():
            return True
        if prints:print("model is not installed, downloading model...")
        dest=str(Path(VMM.models_path).joinpath(model['name']+'.zip'))

        downloaded=_download(model['link'],dest)
        downloaded.start()
        downloaded.wait()
        if downloaded.isFinished():
            if prints:print("Model download completed. installing model...")
            zfile=downloaded.get_dest()
            _ZipFile(zfile).extractall(str(Path(VMM.models_path).joinpath(model['name'])))
            Path(VMM.models_path).joinpath('temp').mkdir(exist_ok=True)
            try:
                orgn=_get_only_folder(Path(VMM.models_path).joinpath(model['name'])).name
                _shutil.move(_get_only_folder(Path(VMM.models_path).joinpath(model['name'])),Path(VMM.models_path).joinpath("temp"))
                temp_folder_name= _get_only_folder(Path(VMM.models_path).joinpath('temp')).name
                _shutil.rmtree(Path(VMM.models_path).joinpath(model['name']))
                _shutil.move(_get_only_folder(Path(VMM.models_path).joinpath('temp')),Path(VMM.models_path))
                _shutil.rmtree(Path(VMM.models_path).joinpath('temp'))
                Path(VMM.models_path).joinpath(temp_folder_name).rename(Path(VMM.models_path).joinpath(model['name']))
            except Exception as err: raise SystemError(err)
            if Path(VMM.models_path).joinpath(orgn):
                if prints:print("Model successfully installed.")
                return True
            else:
                raise SystemError("System failed to install the model.")
        else:
            if prints:print("Model download failed. quiting...")
            return False
    def clear_cache(are_you_sure:bool=False): # This function will remove every zip archive file of models_path folder be ware
        if not are_you_sure:return False
        zip_files = list(Path(VMM.models_path).rglob('*.zip'))
        for zip_file in zip_files:
            if 'vosk' in str(zip_file.absolute()):
                try:
                    zip_file.unlink()
                except:...
        return True
    def clear_folders(are_you_sure:bool=False):
        import warnings,time
        if are_you_sure: warnings.warn(f"You are about to delete all models in the {VMM.models_path}. Please cancel with CTRL+C")
        else:return False
        time.sleep(5)
        print("WARNING: DELETING ALL MODELS, PLEASE DO NOT CANCEL.")
        for item in Path(VMM.models_path).iterdir():
            if item.is_dir():
                _shutil.rmtree(item)
                print(f"Deleted model folder: {item}")
    def _completely_clear_cache(are_you_sure:bool=False):
        import warnings,time
        if are_you_sure: warnings.warn(f"You are about to delete all files/models in the {VMM.models_path}. Please cancel with CTRL+C")
        else:return False
        time.sleep(5)
        print("WARNING: DELETING ALL FILES, PLEASE DO NOT CANCEL.")
        for item in Path(VMM.models_path).iterdir():
            if item.is_dir():
                _shutil.rmtree(item)
                print(f"Deleted folder: {item}")
            else:
                print(f"Deleted file: {item}")
                item.unlink()
        
    def ez_install_model(model_lang:str=Languages.English,model_size:str=VoskModelSize.Small):
        model=VoskModels.GetModel(model_lang,model_size)
        VMM.install_model(model)
    def model_exists(model:dict):
        if Path(VMM.models_path).joinpath(model['name']).exists():
            return True
        return False
    def ez_model_exists(model_lang:str,model_size:str=VoskModelSize.Small):
        return True if perfectdict.has_key(VoskModels.supported_languages,model_lang) and perfectdict.has_key(VoskModels.supported_languages[model_lang],model_size) else False


class WhisperModels:
    available_models=_wa()
    def _winit():
        for model in WhisperModels.available_models:
            setattr(WhisperModels,model.capitalize().replace('-','').replace('.','_'),model)
WhisperModels._winit()