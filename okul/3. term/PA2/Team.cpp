#include "Team.h"

Team::Team()
    : teamID(-1),
      maxLoadCapacity(0),
      currentWorkload(0),
      missionStack(4) {
}

Team::Team(int id, int maxLoad)
    : teamID(id),
      maxLoadCapacity(maxLoad),
      currentWorkload(0),
      missionStack(4) {
}

int Team::getId() const {
    return teamID;
}

int Team::getMaxLoadCapacity() const {
    return maxLoadCapacity;
}

int Team::getCurrentWorkload() const {
    return currentWorkload;
}

void Team::setId(int id) {
    teamID = id;
}

void Team::setMaxLoadCapacity(int maxLoad) {
    maxLoadCapacity = maxLoad;
}

bool Team::hasActiveMission() const {
    return !missionStack.isEmpty();
}

bool Team::tryAssignRequest(const Request& req) {
    //Implement tryAssignRequest function as explained in the PDF.

    if (maxLoadCapacity < currentWorkload + req.computeWorkloadContribution() ){
        //rollbackMission(supplyQueue, rescueQueue); bu işlem qac
        return false;
    } else {
        currentWorkload += req.computeWorkloadContribution();
        missionStack.push(req);
        return true;
    }
    
    //(void)req;
    //return false;
}

void Team::rollbackMission(RequestQueue& supplyQueue, RequestQueue& rescueQueue) {
    //Implement rollbackMission function as explained in the PDF.

    MissionStack tempSupply;
    MissionStack tempRescue;

    Request req;
    
    while(missionStack.pop(req)) 
    {
        if (req.getType() == "SUPPLY") tempSupply.push(req);
        else if (req.getType() == "RESCUE") tempRescue.push(req);
    }

    while (!tempSupply.isEmpty()) { tempSupply.pop(req); supplyQueue.enqueue(req); }

    while (!tempRescue.isEmpty()) { tempRescue.pop(req); rescueQueue.enqueue(req); }

    /*
    while(temp.pop(req)){
        if (req.getType() == "SUPPLY") supplyQueue.enqueue(req);
        else if (req.getType() == "RESCUE") rescueQueue.enqueue(req);
    }*/

    currentWorkload = 0;

    //(void)supplyQueue;
    //(void)rescueQueue;
}


void Team::clearMission() {
    missionStack.clear();
    currentWorkload = 0;
}

const MissionStack& Team::getMissionStack() const {
    return missionStack;
}
