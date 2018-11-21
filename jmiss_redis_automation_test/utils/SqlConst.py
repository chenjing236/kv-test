

class SqlConst:
    class ConstError(TypeError):
        pass

    def __setattr__(self, name, value):
        if name in self.__dict__:
            raise self.ConstError("Can't rebind const (%s)" % name)
        self.__dict__[name] = value


sql_const = SqlConst()

##
## Please write your sql statement here for reference
##
sql_const.QUERY_INSTANCE = "Select * from mc_instance"