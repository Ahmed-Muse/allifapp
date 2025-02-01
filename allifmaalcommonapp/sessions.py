class Allifsessions():
    def __init__(self,request,*name):
        self.session=request.session
        self.name=name
        # get the current session key if it exists.
        user_session=self.session.get('user_session_key')
        
       
        # if the user is new, then no session key, so create one.
        if 'user_session_key' not in request.session:
            user_session=self.session['user_session_key']={}

        # lets make sure that the user session is available on all pages of the site.
        self.user_session=user_session
    #obj=Allifsessions("","ahmed")