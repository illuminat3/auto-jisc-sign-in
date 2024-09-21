import psutil
import platform
import hashlib

class SystemProfiler:
    @staticmethod
    def GetCoreCount():
        return psutil.cpu_count(logical=True)
    
    @staticmethod
    def GetUniqueID():
        system_info = []
        system_info.append(platform.system())    
        system_info.append(platform.node())  
        system_info.append(platform.release())    
        system_info.append(platform.version())  
        system_info.append(platform.machine())     

        combined_info = ''.join(system_info)

        hashed_info = hashlib.sha256(combined_info.encode()).hexdigest()
        unique_id = int(hashed_info[:8], 16) 
        return str(unique_id).zfill(8)