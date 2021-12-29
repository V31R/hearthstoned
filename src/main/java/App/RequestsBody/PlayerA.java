package App.RequestsBody;

import javax.validation.constraints.NotBlank;

public class PlayerA {


    @NotBlank
    private String battleTag;

    @NotBlank
    private String stringedAuthorizationID;
    @NotBlank
    private String authorizationType;

    public String getAuthorizationType() {
        return authorizationType;
    }

    public void setAuthorizationType(String authorizationType) {
        this.authorizationType = authorizationType;
    }

    public String getStringedAuthorizationID() {
        return stringedAuthorizationID;
    }

    public void setStringedAuthorizationID(String uid) {
        this.stringedAuthorizationID = uid;
    }


    public String getBattleTag() {
        return battleTag;
    }

    public void setBattleTag(String battleTag) {
        this.battleTag = battleTag;
    }


}
