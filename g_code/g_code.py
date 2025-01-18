import logging


logger = logging.getLogger(__name__)




class GCodeLine:
    def __init__(self, raw : str):
        self.raw = raw
        self.command = tuple() # ('G', 1)
        self.params = {}       # {'X' : -90, 'Y' : -45}
        self.comment = None
        self.parse()

    def parse(self):
        if ';' in self.raw:
            code, comment = self.raw.split(';', 1)
            #logger.debug(f'Code: {code}, Comment: {comment}')
            self.comment = comment.strip()
        else:
            code = self.raw

        code = code.split()
        self.command = (code[0][0], int(code[0][1:]))

        for p in code[1:]:
            self.params[p[0]] = float(p[1:])
        logger.debug(self)

    def __str__(self):
        return f'{self.command[0]}{self.command[1]} {self.params}'


        
class GCode:
    def __init__(self, raw):
        """
        C00 P0 Q0;  Comment
        """
        self.raw = raw
        self.lines = []
        self.parse()

    def parse(self):
        lines = self.raw.split('\n')
        assert lines[0] == lines[-1] == '%'
        for l in lines[1:-1]:
            self.lines.append(GCodeLine(l))


if __name__ == "__main__":
    import sys
    logging.basicConfig(level=logging.DEBUG)
    print(sys.argv)
    if len(sys.argv) > 1:
        file_path = sys.argv[1]
    else:
        sys.exit(1)
    logger.info(f'Reading file: {file_path}')
    with open(file_path) as f:
        g_code = GCode(f.read())
    #for l in g_code:
    #    logger.info(l)