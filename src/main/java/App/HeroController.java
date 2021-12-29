package App;

import App.Data.GetsHeroesStat;
import App.Data.GetsHeroesStatRepository;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

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

    @GetMapping("/{BattleTag}")
    public List<GetsHeroesStat> getListHeroesAtPlayers(@PathVariable("BattleTag") String battleTag){

        return getsHeroesStatRepository.findAll().stream().filter((h)->(h.getBattleTag()!=null && h.getBattleTag().equals(battleTag))).toList();

    }


}
