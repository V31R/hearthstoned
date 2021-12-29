package App;

import App.Data.GetsHeroesStat;
import App.Data.GetsHeroesStatRepository;
import App.RequestsBody.BattleTag;
import org.springframework.web.bind.annotation.*;

import java.util.List;

@RestController
@RequestMapping("/heroes")
public class HeroController {

    private GetsHeroesStatRepository getsHeroesStatRepository;

    public HeroController(GetsHeroesStatRepository getsHeroesStatRepository) {

        this.getsHeroesStatRepository = getsHeroesStatRepository;

    }

    @GetMapping("")
    public List<GetsHeroesStat> getListHeroes(){

        return getsHeroesStatRepository.findAll();

    }

    @GetMapping("/player")
    public List<GetsHeroesStat> getListHeroesAtPlayers(@RequestBody BattleTag tag){

        return getsHeroesStatRepository.findAll().stream().filter((h)->(h.getBattleTag()!=null && h.getBattleTag().equals(tag.getTagValue()))).toList();

    }


}
