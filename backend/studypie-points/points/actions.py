class Actions(object):
  SIGN_UP = 0
  CREATE_POST = 1
  CREATE_COMMENT = 2

  def __contains__(self, target):
    return target in self.__class__.__dict__.values()


actions = Actions()

action_choices = (
    (actions.SIGN_UP, 'sign up'),
    (actions.CREATE_POST, 'create post'),
    (actions.CREATE_COMMENT, 'create comment'),
)
