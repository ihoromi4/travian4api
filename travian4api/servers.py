
class Servers:
    def __getattr__(self, key):
        if not type(key) is str:
            raise TypeError('attribute must be str')
            
        if not '_' in key:
            raise ValueError('value must be \'_\' separated')
            
        result = key.split('_')
        result = [part.lower() for part in result]
        result.insert(1, 'travian')
        return '.'.join(result)

servers = Servers()

