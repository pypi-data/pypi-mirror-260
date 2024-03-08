
class ScikitProperty():
    """ Quantitative Information extract from Regions Properties from scikit image
    Parameters
    ----------
    name : string
        the name of the info
    type : string
        the type of the info as definied in the MorphoNet format  https://morphonet.org/help_format

    """

    def __init__(self, dataset, name,type):
        self.name = name
        self.dataset = dataset
        self.data = {}
        self.computed_times = {}
        self.updated = False
        self.asked = False
        self.type = type
        self.sent=False

    def delete(self,mo):
        if mo.t in self.data and mo in self.data[mo.t]:
            self.data[mo.t].pop(mo.t)


    def set(self,mo,value):
        if mo.t not in self.data: self.data[mo.t]={}
        if mo.channel not in self.data[mo.t]:  self.data[mo.t][mo.channel]={}
        self.data[mo.t][mo.channel][mo] = value
        self.updated=True

    def get(self,mo):
        if mo.t not in self.data: return None
        if mo.channel not in self.data[mo.t]: return None
        if mo not in  self.data[mo.t][mo.channel]: return None
        return self.data[mo.t][mo.channel][mo]

    def get_at(self,t,channel):
        if t not in self.data: return None
        if channel not in self.data[t]: return None
        return self.data[t][channel]

    def del_at(self, t, channel):
        if t not in self.data: return False
        if channel not in self.data[t]: return False
        self.data[t].pop(channel)
        return True

    def del_cell(self, mo):
        if mo.t not in self.data: return False
        if mo.channel not in self.data[mo.t]: return False
        if mo not in self.data[mo.t][mo.channel]: return False
        self.data[mo.t][mo.channel].pop(mo)
        return True

    def get_txt(self):
        Text =  "#MorphoPlot" + '\n'
        Text += "#"+self.name+" property computed from Scikit image\n"
        Text += "type:" + self.type + "\n"
        for t in self.data:
            for c in self.data[t]:
                for o in self.data[t][c]:
                    if o.id!=self.dataset.background:
                        Text += o.get_name() + ':' + str(self.data[t][c][o])
                        Text += '\n'
        return Text
