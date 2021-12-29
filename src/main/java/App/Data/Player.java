package App.Data;

import javax.persistence.*;

@Entity
@Table(name = "player")
public class Player {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "player_id", nullable = false)
    private Integer id;


    @Column(name = "BattleTag", nullable = false)
    private String battleTag;

    public Integer getId() { return id; }

    public void setId(Integer id) {
        this.id = id;
    }

    public String getBattleTag() {

        return battleTag;

    }

}