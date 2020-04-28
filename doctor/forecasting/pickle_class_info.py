class SerializableData:
    def __init__(self,train_df,model,label):
        self.label=label
        self.train_df=train_df
        self.model=model
    def getItems(self):
        return (self.label,self.train_df,self.model)
