package App.RequestsBody;

import javax.validation.constraints.NotBlank;

public class BattleTag {

    @NotBlank
    private String tagValue;

    public String getTagValue() {

        return tagValue;

    }

    public void setTagValue(String tagValue) {

        this.tagValue = tagValue;

    }


}
