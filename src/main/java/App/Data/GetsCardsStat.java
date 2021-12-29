package App.Data;

import com.fasterxml.jackson.annotation.JsonIgnore;

import javax.persistence.Column;
import javax.persistence.Entity;
import javax.persistence.Id;
import javax.persistence.Table;
import java.math.BigDecimal;

@Entity
//@Immutable
@Table(name = "gets_cards_stats")
public class GetsCardsStat {
    //@Id
    @Column(name = "cardURL", length = 62)
    private String cardID;

    @Column(name = "name", nullable = false, length = 50)
    private String cardName;

    @Column(name = "win_rate", precision = 26, scale = 2)
    private BigDecimal winRate;

    @Column(name = "avg_pos", precision = 14, scale = 4)
    private BigDecimal averagePosition;

    @Column(name = "attack", nullable = false)
    private Integer attack;

    @Column(name = "health", nullable = false)
    private Integer health;

    @Column(name = "tech_level", nullable = false)
    private Integer techLevel;

    @Column(name = "card_text", length = 250)
    private String cardText;

    @Column(name = "c_race", nullable = false, length = 20)
    private String cardRace;

    @Column(name = "heroURL", length = 63)
    private String heroID;

    @Column(name = "hero_name", length = 50)
    private String heroName;

    @Column(name = "flavor_text", length = 250)
    private String flavorText;

    @JsonIgnore
    @Column(name = "BattleTag", length = 50)
    private String battleTag;

    @JsonIgnore
    @Id
    @Column(name = "id", length = 62)
    private String id;

    GetsCardsStat(){}

    public String getFlavorText() {
        return flavorText;
    }

    public String getHeroName() {
        return heroName;
    }

    public String getHeroID() {
        return heroID;
    }

    public String getCardRace() {
        return cardRace;
    }

    public String getCardText() {
        return cardText;
    }

    public Integer getTechLevel() {
        return techLevel;
    }

    public Integer getHealth() {
        return health;
    }

    public Integer getAttack() {
        return attack;
    }

    public BigDecimal getAveragePosition() {
        return averagePosition;
    }

    public BigDecimal getWinRate() {
        return winRate;
    }

    public String getCardName() {
        return cardName;
    }

    public String getCardID() {
        return cardID;
    }

    public String getBattleTag() {return battleTag;}

}