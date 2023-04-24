package io.github.nandandesai.pico.repositories;

import io.github.nandandesai.pico.models.Role;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;

@Repository
public interface RoleRepository extends JpaRepository<Role, String> {

}
