package App.Data;

import com.fasterxml.jackson.annotation.JsonIgnore;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import java.math.BigDecimal;

@Entity
//@Immutable
@Table(name = "gets_heroes_stats")
public class GetsHeroesStat {
    //@Id
    @Column(name = "heroID", length = 63)
    private String heroID;

    @Column(name = "name", nullable = false, length = 50)
    private String heroName;

    @Column(name = "win_rate", precision = 26, scale = 2)
    private BigDecimal winRate;

    @Column(name = "avg_position", precision = 37, scale = 2)
    private BigDecimal averagePosition;

    @Column(name = "selection_frequency", precision = 31, scale = 2)
    private BigDecimal selectionFrequency;

    @Column(name = "health", nullable = false)
    private Integer health;

    @Column(name = "hp_name", nullable = false, length = 50)
    private String heroPowerName;

    @Column(name = "hp_text", length = 400)
    private String heroPowerText;

    @Column(name = "hp_cost")
    private Integer heroPowerCost;


    @Column(name = "hpURL", length = 67)
    private String heroPowerID;

    @Column(name = "rating_change", precision = 32)
    private BigDecimal ratingChange;

    @JsonIgnore
    @Column(name = "BattleTag", length = 50)
    private String battleTag;

    @JsonIgnore
    @Id
    @Column(name = "id", length = 62)
    private String id;

    public BigDecimal getRatingChange() {
        return ratingChange;
    }

    public String getHeroPowerID() {
        return heroPowerID;
    }

    public Integer getHeroPowerCost() {
        return heroPowerCost;
    }

    public String getHeroPowerText() {
        return heroPowerText;
    }

    public String getHeroPowerName() {
        return heroPowerName;
    }

    public Integer getHealth() {
        return health;
    }

    public BigDecimal getSelectionFrequency() {
        return selectionFrequency;
    }

    public BigDecimal getAveragePosition() {
        return averagePosition;
    }

    public BigDecimal getWinRate() {
        return winRate;
    }

    public String getHeroName() {
        return heroName;
    }

    public String getHeroID() {
        return heroID;
    }

    public String getBattleTag() {return battleTag;}

}