from .backend import get_config, logger

class Error(Exception):
    def __init__(this, objname:str, title:str, msg:str, *args:object):
        fullmsg = "Object {} error: ({}) {}".format(objname, title, msg)
        log.throwerr(title, True, msg)
        super().__init__(fullmsg, *args)

class AppSettings(object):
    
    def __init__(this,
                 cfg:dict=get_config.cfg,
                 file:str=get_config.file,
                 default_section:str=(item[0] for item, item2 in get_config.cfg.items()),
                 **kwds
    ):
        this.cfg = get_config.GetConfig(
            cfg,
            file,
            default_section=default_section,
            **kwds
        )
    
    def get_setting(this, sectionname, option, needed:bool=False):
        return this.cfg.getkey(sectionname, option, needed)
    
    def set_setting(this, section, option, value):
        return this.cfg.set(section, option, value)
    
    def register_section(this, section_name, options: dict):
        """Register a new section on the configuration file."""
        this.cfg.add_section(section_name)
        this.cfg[section_name] = options
    
    def unregister_section(this, section_name):
        """Unregister a section on the configuration file."""
        return this.cfg.remove_section(section_name)

global_settings = AppSettings()
log = logger.Logger()