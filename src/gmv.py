'''
Created on Dec 16, 2011

@author: guillaume.aubert@gmail.com
'''
from cmdline_utils  import CmdLineParser


HELP_USAGE = """ gmvault [options]
                                     
Arguments: a list of request files or an inline request."""

HELP_EPILOGUE = """Examples:

a) full synchronisation with email and password login

#> gmvault --email foo.bar@gmail.com --passwd vrysecrtpasswd 

b) full synchronisation for german users that have to use googlemail instead of gmail

#> gmvault --imap-server imap.googlemail.com --email foo.bar@gmail.com --passwd sosecrtpasswd
"""

class GMVaultLauncher(object):
    
    def __init__(self):
        """ constructor """
        super(GMVaultLauncher, self).__init__()

    def parse_args(self):
        """ Parse command line arguments 
            
            :returns: a dict that contains the arguments
               
            :except Exception Error
            
        """
        #print sys.argv
        
        parser = CmdLineParser()
        
        parser.add_option("-s", "--sync", help = "full synchronisation between gmail with local db. (default sync mode)", \
                          action ="store_true", dest="sync", default= False)
        
        parser.add_option("-q", "--quick-sync", help = "quick synchronisation between  gmail with local db", \
                          action ="store_true", dest="qsync", default= False)
        
        parser.add_option("-n", "--inc-sync", help = "incremental synchronisation between gmail with local db", \
                          action ="store_true", dest="isync", default= False)
        
        parser.add_option("-i", "--imap-server", \
                          help="gmail imap server hostname",\
                          dest="host", default="imap.gmail.com")
        
        parser.add_option("-r", "--imap-port", \
                          help="gmail imap server port",\
                          dest="port", default=993)
        
        parser.add_option("-l", "--email", \
                          help="gmail email",\
                          dest="email", default=None)
        
        parser.add_option("-p", "--passwd", \
                          help="gmail password",\
                          dest="passwd", default=None)
        
        parser.add_option("-d", "--db-dir", \
                          help="database root directory",\
                          dest="db_dir", default="./gmvault")
        
        parser.add_option("-o", "--oauth-token", \
                          help="oauth-token",\
                          dest="oauth_token", default=None)
        
        parser.add_option("-v", "--verbose", \
                          help="Activate the verbose mode.",\
                          action="store_true", dest="verbose", default=False)
       
        """
        dir_help =  "Directory where the result files will be stored.".ljust(66)
        dir_help += "(Default =. the current dir)".ljust(66)
        dir_help += "The directory will be created if it doesn't exist.".ljust(66)
        
        parser.add_option("-d", "--dir", metavar="DIR", \
                          help = dir_help,\
                          dest ="output_dir", default=".")
        """
        
        # add custom usage and epilogue
        parser.epilogue = HELP_EPILOGUE
        parser.usage    = HELP_USAGE
        
        (options, args) = parser.parse_args() #pylint: disable-msg=W0612
        
        parsed_args = { }
        
        #check the sync mode
        if options.qsync:
            parsed_args['sync-mode'] = 'qsync'
        elif options.isync:
            parsed_args['sync-mode'] = 'isync'
        else:
            parsed_args['sync-mode'] = 'sync'
        
        # add host
        parsed_args['host']             = options.host
        
        # add login
        parsed_args['email']            = options.email
        
        
        # Cannot have passwd and oauth-token at the same time
        if options.passwd and options.oauth_token:
            self.error("Only one authentication mode can be used (password or oauth-token)")
        
        # add passwd
        parsed_args['passwd']           = options.passwd

        # add oauth token
        parsed_args['oauth-token']      = options.oauth_token
        
        # add passwd
        parsed_args['db-dir']           = options.db_dir
     
        #verbose
        parsed_args['verbose']          = options.verbose
        
        #add parser itself for error handling
        parsed_args['parser'] = parser
        
        return parsed_args
    
    def run(self, args):
        """
           Run the grep with the given args 
        """
        print("In run. Args = %s\n" %(args))
    
def bootstrap_run():
    """ temporary bootstrap """
    
    gmvault = GMVaultLauncher()
    
    args = gmvault.parse_args()
    
    gmvault.run(args)
   
    
if __name__ == '__main__':
    import sys
    sys.argv = ['gmvault.py', '--sync','--host', 'imap.gmail.com', '--port', '1452', '--login', 'foo', '--passwd', 'bar']
    
    print(sys.argv)
    
    bootstrap_run()
    
    sys.exit(0)
