
class UserInfo:
    id: str
    pw: str
    name: str
    stage: int
    phone: str
    alarm: str

    def Set_User(self, id: str, pw: str, name: str, phone: str, stage: str, alarm: str):
        self.id = id
        self.pw = pw
        self.name = name
        self.stage = stage
        self.phone = phone
        self.alarm = alarm
        
user = UserInfo()
