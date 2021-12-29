package App.Data;

import com.sun.xml.bind.v2.model.core.ID;
import org.springframework.data.jpa.repository.JpaRepository;

public interface GetsCardsStatRepository extends JpaRepository<GetsCardsStat, ID> {
}