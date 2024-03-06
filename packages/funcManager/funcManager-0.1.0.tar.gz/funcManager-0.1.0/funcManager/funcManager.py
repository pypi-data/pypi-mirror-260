import inspect
import traceback

class funcManager:
    funcIgnore = []

    file = traceback.extract_stack()[0].filename

    #get all functions in the currect script
    def getFunctions(self):
        me = __import__(inspect.getmodulename(self.file))
        funcList = [getattr(me, name) for name in dir(me) if inspect.isclass(getattr(me, name))]
        functions = {}
        for func in funcList:
            if func.__name__ not in self.funcIgnore:
                functions[str(func.__name__).lower()] = func
        return functions