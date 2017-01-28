from urllib.parse import urlparse, parse_qs


class MagnetUrl(object):
    url = None
    xturn_delimiter = ':'

    def __init__(self, url):
        self.url = url

    @property
    def files(self):
        '''Returns list of files contained in magnet url
        Files are dicts with following fields:
        hash_type
        hash
        data_size
        display_name
        All fields are currently optional and can be None'''
        files = []
        index = 0
        #: lambda checks if entry is valid
        has_data = lambda e: any([x is not None for x in list(e.values())])
        entry = self.__file_entry(0)
        while has_data(entry):
            files.append(entry)
            index += 1
            entry = self.__file_entry(index)
        return files

    @property
    def trackers(self):
        return self.data.get('tr', [])

    @property
    def acceptable_sources(self):
        return self.data.get('xs', [])

    # Private side of implementation
    @property
    def data(self):
        '''Tries to parse url, implements simple caching of value
        to avoid reparsing on every property's access'''
        if hasattr(self, '_data'):
            return getattr(self, '_data')
        self._data = self.__parse(self.url)
        return self._data

    def __parse(self, url):
        parsed = urlparse(url)
        if parsed.scheme != 'magnet':
            return {}
        #: There are differencies in behaviour of urlparse
        #: between interpreters and python versions so we must assume
        #: that magnet data may be in these two properties.
        data = parse_qs(parsed.query or parsed.path[1:])
        query_data = {}
        for param_name, values_list in list(data.items()):
            #we're unpacking values
            if len(values_list) == 1:
                query_data[param_name] = values_list[0]
            else:
                query_data[param_name] = values_list
        return query_data

    def __display_name(self, index=None):
        return self.data_index('dn', index)

    def data_index(self, fieldname, index=None):
        data_fieldname = "%s.%s" % (fieldname, index) if index else fieldname
        return self.data.get(data_fieldname)

    def __hash_type(self, index=None):
        ''' Returns type of hash used in magnet link. i.e for 
        xt=urn:btih:hash_value "btih" is returned.
        In case of multi-partial names like:
        xt=urn:tree:tiger:hash_value
        concatenation is returned, 'tree tiger' in this case.'''
        xturn = self.data_index('xt', index)
        if not xturn:
            return
        return ' '.join(xturn.split(self.xturn_delimiter)[1:-1])

    def __hash(self, index=None):
        '''Returns hash value used in magnet link. Currently we assume that
        hash is the last part of xt(.<index>) URN.
        For: 
        xt=urn:tree:tiger:hash_value
        function returns hash_value or none
        '''
        xturn = self.data_index('xt', index)
        if not xturn:
            return
        return xturn.split(self.xturn_delimiter)[-1]

    def __data_size(self, index=None):
        '''Tries to return data-size if is provided'''
        return self.data_index('xl', index)

    def __file_entry(self, index):
        return dict(
            display_name=self.__display_name(index),
            data_size=self.__data_size(index),
            hash_type=self.__hash_type(index),
            hash=self.__hash(index))
