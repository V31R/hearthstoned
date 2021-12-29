package App;

import App.Data.GetsCardsStat;
import App.Data.GetsCardsStatRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;

@RestController
@RequestMapping("/cards")
public class CardController {

    private GetsCardsStatRepository getsCardsStatRepository;

    public CardController(GetsCardsStatRepository getsCardsStatRepository) {

        this.getsCardsStatRepository = getsCardsStatRepository;

    }


    @GetMapping("")
    public List<GetsCardsStat> getListHeroes(){

        return getsCardsStatRepository.findAll();

    }

    @GetMapping("/{name}/{tag}")
    public List<GetsCardsStat> getListHeroesAtPlayers(@PathVariable("name") String name,@PathVariable("tag") String tag){

        String battleTag= new String(name+"#"+tag);

        return getsCardsStatRepository.findAll().stream().filter((c)->(c.getBattleTag()!=null && c.getBattleTag().equals(battleTag))).toList();

    }

}
