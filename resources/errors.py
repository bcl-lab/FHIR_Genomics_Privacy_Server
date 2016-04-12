from flask_restful import abort


class PrivacyServerError():
    def __init__(self):
        pass

    def abort_with_unaccessable_error(self):
        abort(404, message= "You cannot get privacy list for multiple targets")

    def abort_with_authenticate_error(self):
        pass

    def abort_with_POST_error(self):
        abort(404, message= "The data submitted lack some essential parts or does not meet the requirement")


    def abort_with_search_error(self,identifier):
        abort(404, message= "The policy for this patient {} is not in database, please check your posted data".format(identifier))

    def abort_with_Scope_error(self):
        abort(404, message= "You should provide at least one Scope in the following one : Clinician/Researcher/Patient/Commercial")