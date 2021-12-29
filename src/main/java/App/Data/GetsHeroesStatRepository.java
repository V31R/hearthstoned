package App.Data;

import com.sun.xml.bind.v2.model.core.ID;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface GetsHeroesStatRepository extends JpaRepository<GetsHeroesStat, ID> {
}