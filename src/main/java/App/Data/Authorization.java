package App.Data;

import com.fasterxml.jackson.annotation.JsonIgnore;

import javax.persistence.*;

@Entity
@Table(name = "authorization")
public class Authorization {
    @JsonIgnore
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    @Column(name = "authorization_id", nullable = false)
    private Integer id;

    @ManyToOne
    @JoinColumn(name = "player_id")
    private Player BattleTag;

    @Column(name = "uid", length = 100)
    private String stringedAuthorizationID;

    @Column(name = "type", length = 100)
    private String authorizationType;

    public String getAuthorizationType() {
        return authorizationType;
    }

    public void setAuthorizationType(String authorizationType) {
        this.authorizationType = authorizationType;
    }

    public String getUid() {
        return stringedAuthorizationID;
    }

    public void setUid(String uid) {
        this.stringedAuthorizationID = uid;
    }

    public Player getBattleTag() {
        return BattleTag;
    }

    public void setBattleTag(Player battleTag) {
        this.BattleTag = battleTag;
    }

    public Integer getId() {
        return id;
    }

    public void setId(Integer id) {
        this.id = id;
    }
}