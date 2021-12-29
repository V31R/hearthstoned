package App;

import App.Data.*;
import App.UserException.UserNotFoundException;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/users")
public class AuthorizationController {

    private AuthorizationRepository authorizationRepository;
    private PlayerRepository playerRepository;

    public AuthorizationController(AuthorizationRepository authorizationRepository, PlayerRepository playerRepository) {

        this.authorizationRepository = authorizationRepository;
        this.playerRepository=playerRepository;

    }


    @PostMapping("")
    public void authorize(@RequestBody PlayerA user){


        List<Player> players=playerRepository.findAll().stream()
                .filter((p)->p.getBattleTag().equals(user.getBattleTag())).toList();

        if(players.size()==0){

            throw new UserNotFoundException("BattleTag "+user.getBattleTag());

        }

        List<Authorization> authorizations= authorizationRepository.findAll()
                .stream()
                .filter((a)->a.getBattleTag().getBattleTag().equals(user.getBattleTag()) &&
                        a.getAuthorizationType().equals(user.getAuthorizationType()))
                .toList();

        if(authorizations.size()==0){

            Authorization newUser=new Authorization();
            newUser.setAuthorizationType(user.getAuthorizationType());
            newUser.setBattleTag(
                    playerRepository.findAll().stream()
                    .filter((p)->p.getBattleTag().equals(user.getBattleTag())).findFirst().get());
            newUser.setUid(user.getStringedAuthorizationID());
            authorizationRepository.save(newUser);

        }
        else{

            List<Authorization> auth=authorizations.stream()
                    .filter((a)->a.getUid().equals(user.getStringedAuthorizationID()))
                    .toList();
            if(auth.size()==0){

                throw new UserNotFoundException("already registered at "+user.getAuthorizationType());

            }else{

                //return ;

            }


        }
        //return user;

    }



}
