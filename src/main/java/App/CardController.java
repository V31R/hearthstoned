package App;

import App.Data.GetsCardsStat;
import App.Data.GetsCardsStatRepository;
import App.RequestsBody.BattleTag;
import App.RequestsBody.PlayerA;
import org.springframework.web.bind.annotation.*;

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

    @PostMapping("/player")
    public List<GetsCardsStat> getListHeroesAtPlayers(@RequestBody BattleTag tag){

        return getsCardsStatRepository.findAll().stream().filter((c)->(c.getBattleTag()!=null
                && c.getBattleTag().equals(tag.getTagValue()))).toList();

    }

}
