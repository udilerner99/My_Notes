package com.keysoft.bucktrackerjpa.dao;

import com.keysoft.bucktrackerjpa.entity.Application;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.stereotype.Repository;
import org.springframework.web.bind.annotation.PutMapping;
import org.springframework.web.bind.annotation.RequestBody;

import javax.persistence.EntityManager;
import javax.persistence.PersistenceContext;
import javax.transaction.Transactional;
import java.util.List;

@Transactional
@Repository
public class ApplicationDAO implements  IApplicationDAO {

    @PersistenceContext
    private EntityManager entityManager;

    @Override
    public void addApplication(Application application) {
        entityManager.persist(application);
    }

    @Override
    public boolean applicationExists(String name, String owner) {
        //note application is the class name; not the table name; class name is case sensitive; use class field names - column names
        String jpql = "from Application as a WHERE a.name = ? and a.owner = ?";
        int count = entityManager.createQuery(jpql).setParameter(0, name).setParameter(1, owner).getResultList().size();
        return count > 0;
    }

    @Override
    public Application getApplicationById(int applicationId) {
        return entityManager.find(Application.class, applicationId);
    }

    @Override
    public void updateApplication(Application application) {
        Application app = getApplicationById(application.getId());
        app.setName(application.getName());
        app.setDescription(application.getDescription());
        app.setOwner(application.getOwner());
        entityManager.flush();
    }

    @Override
    public void deleteApplication(int applicationId) {
       //TODO implement deleting an application using the EntityManager

    }

}
