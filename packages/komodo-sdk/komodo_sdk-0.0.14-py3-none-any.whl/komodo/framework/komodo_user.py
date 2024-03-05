class KomodoUser:
    def __init__(self, email, name,
                 role=None, plan=None, verified=True, allowed_assistants=None, preferred_assistant=None):
        self.email = email
        self.name = name
        self.role = role
        self.plan = plan
        self.verified = verified
        self.allowed_assistants = allowed_assistants
        self.preferred_assistant = preferred_assistant

    def __str__(self):
        return f"KomodoUser(email={self.email}, name={self.name}, role={self.role}, plan={self.plan}, verified={self.verified}, allowed_assistants={self.allowed_assistants}, preferred_assistant={self.preferred_assistant})"

    def to_dict(self):
        return {
            'email': self.email,
            'name': self.name,
            'role': self.role,
            'plan': self.plan,
            'verified': self.verified,
            'allowed_assistants': self.allowed_assistants,
            'preferred_assistant': self.preferred_assistant}

    @classmethod
    def default_user(cls):
        shortcode = "ryan"
        email = "ryan.oberoi@komodoapp.ai"
        return cls(email=email, name="Ryan Oberoi", role="user", plan="free", verified=True,
                   allowed_assistants=[], preferred_assistant="")
