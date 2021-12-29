package App.UserException;

public class UserNotFoundException extends  RuntimeException{

    public UserNotFoundException(String what){

        super("Could not find player with " + what);

    }

}
