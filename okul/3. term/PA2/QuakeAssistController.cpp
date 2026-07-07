#include "QuakeAssistController.h"
#include <iostream>
#include <sstream>

QuakeAssistController::QuakeAssistController()
    : teams(nullptr),
      teamCount(0),
      supplyQueue(4),
      rescueQueue(4) {
}

QuakeAssistController::~QuakeAssistController() {
    delete[] teams;
}

bool QuakeAssistController::parseAndExecute(const std::string& line) {
    //Read the input file line by line and execute realtime.
    std::stringstream ss(line);
    std::string cmd;
    ss >> cmd;

    if (cmd == "INIT_TEAMS") {
        int numTeams;
        ss >> numTeams;
        initializeTeams(numTeams);
    }

    else if (cmd == "SET_TEAM_CAPACITY") {
        int teamID, maxLoadCapacity;
        ss >> teamID >> maxLoadCapacity;
        handleSetTeamCapacity(teamID, maxLoadCapacity);
    }

    else if (cmd == "ADD_SUPPLY") {
        std::string id, city, supplyType;
        int amount, emergencyLevel;
        ss >> id >> city >> supplyType >> amount >> emergencyLevel;
        handleAddSupply(id, city, supplyType, amount, emergencyLevel);
    }

    else if (cmd == "ADD_RESCUE") {
        std::string id, city, buildingRisk;
        int numPeople, emergencyLevel;
        ss >> id >> city >> numPeople >> buildingRisk >> emergencyLevel;
        handleAddRescue(id, city, numPeople, buildingRisk, emergencyLevel);
    }

    else if (cmd == "REMOVE_REQUEST") {
        std::string id;
        ss >> id;
        handleRemoveRequest((std::string&)id);
    }

    else if (cmd == "HANDLE_EMERGENCY") {
        int teamID, k;
        ss >> teamID >> k;
        handleHandleEmergency(teamID, k);
    }

    else if (cmd == "DISPATCH_TEAM") {
        int teamID;
        ss >> teamID;
        handleDispatchTeam(teamID);
    }

    else if (cmd == "PRINT_QUEUES") {
        printQueues();
    }

    else if (cmd == "PRINT_TEAM") {
        int teamID;
        ss >> teamID;
        printTeam(teamID);
    }

    else if (cmd == "CLEAR") {
        clear();
    }

    else {
        std::cout << "Error: Unknown command '" << cmd << "'.\n";
        return false;
    }

    return true;
}

bool QuakeAssistController::initializeTeams(int numTeams) {
    //Create a team array and initialize it with teams.
    
    //Initializes the system with numTeams teams. Any previously existing teams are cleared.
    if (teams != nullptr) {
        delete[] teams;
    }

    teams = new Team[numTeams];
    teamCount = numTeams;

    for (int i = 0; i < numTeams; i++) {
        teams[i].setId(i);
    }

    std::cout << "Initialized " << numTeams << " teams.\n";
    return true;
}

int QuakeAssistController::findTeamIndexById(int teamId) const {
    //Find the index of the team using teamId.
    if (teams == nullptr || teamCount == 0)
        return -1;
    
    if (teamId < 0 || teamId >= teamCount)
        return -1;

    return teamId;
}

bool QuakeAssistController::handleSetTeamCapacity(int teamId, int capacity) {
    //Find the index of team in the array, update the capacity value of the team.
    int idx = findTeamIndexById(teamId);
    if (idx == -1) {
        std::cout << "Error: Invalid team ID.\n";
        return false;
    }

    Team& team = teams[idx];
    team.setMaxLoadCapacity(capacity);

    std::cout << "Team " << idx << " capacity set to " << capacity << ".\n";
    return true;
}

bool QuakeAssistController::handleAddSupply(const std::string& id,
                                            const std::string& cityStr,
                                            const std::string& supplyTypeStr,
                                            int amount,
                                            int emergencyLevel) {
    //City city = stringToCity(cityStr);
    //SupplyType st = stringToSupplyType(supplyTypeStr);
    //Create new supply request, and add it to the SUPPLY queue.

    Request req(id, cityStr, supplyTypeStr, amount, emergencyLevel);
    supplyQueue.enqueue(req);

    std::cout << "Request " << id << " added to SUPPLY queue.\n";
    return true;
}

bool QuakeAssistController::handleAddRescue(const std::string& id,
                                            const std::string& cityStr,
                                            int numPeople,
                                            const std::string& riskStr,
                                            int emergencyLevel) {
    //City city = stringToCity(cityStr);
    //BuildingRisk risk = stringToBuildingRisk(riskStr);
    //Create new rescue request, and add it to the RESCUE queue.

    Request req(id, cityStr, numPeople, riskStr, emergencyLevel);
    rescueQueue.enqueue(req);

    std::cout << "Request " << id << " added to RESCUE queue.\n";
    return true;
}

bool QuakeAssistController::handleRemoveRequest(const std::string& id) {
    //Remove request using request ID from request(SUPPLY, RESCUE) queue. 

    /*If REMOVE_REQUEST cannot find a given ID in either queue, the following message must be
    printed:
    Error: Request <id> not found.*/

    bool removedFromSupply = supplyQueue.removeById(id);
    bool removedFromRescue = rescueQueue.removeById(id);

    if (!removedFromSupply && !removedFromRescue) {
        std::cout << "Error: Request " << id << " not found.\n";
        return false;
    }

    std::cout << "Request " << id << " removed.\n";
    return true;
}

bool QuakeAssistController::handleHandleEmergency(int teamId, int k) {
    // TODO: Implement:
    // 1) Find team by id.
    // 2) For up to k steps:
    //    - Look at front of supplyQueue and rescueQueue using peek().
    //    - Use Request::computeEmergencyScore() to decide which to take.
    //    - If both empty -> break.
    //    - Try teams[teamIdx].tryAssignRequest(chosenRequest).
    //       * If this returns false, print overload message and
    //         call teams[teamIdx].rollbackMission(supplyQueue, rescueQueue),
    //         then break.
    //       * Else, dequeue chosen request from its queue and continue.

    int idx = findTeamIndexById(teamId);
    if (idx == -1) {
        std::cout << "Error: Invalid team ID.\n";
        return false;
    }

    Team& team = teams[idx];

    int assignedSupply = 0;
    int assignedRescue = 0;

    for (int i = 0; i < k; ++i) {
        Request reqSupp;
        bool hasSupply = supplyQueue.peek(reqSupp);

        Request reqRes;
        bool hasRescue = rescueQueue.peek(reqRes);

        if (!hasSupply && !hasRescue)
            break;

        
        Request emergency;
        bool isSupply = false;
        

        if (hasSupply && hasRescue){
            if (reqRes.computeEmergencyScore() >= reqSupp.computeEmergencyScore()){
                emergency = reqRes;
                isSupply = false;
            }else {
                emergency = reqSupp;
                isSupply = true;
            }
        }else if (hasSupply) {
            emergency = reqSupp;
            isSupply = true;
        } else { 
            emergency = reqRes;
            isSupply = false;
        }

        bool ok = team.tryAssignRequest(emergency);
        if(!ok){
            std::cout << "Overload on Team " << teamId << ": rolling back mission.\n";
            team.rollbackMission(supplyQueue, rescueQueue);
            return true;
        }

        Request dummy;
        if (isSupply) {
            supplyQueue.dequeue(dummy);
            ++assignedSupply;
        } else {
            rescueQueue.dequeue(dummy);
            ++assignedRescue;
        }

    }

    int totalAssigned = assignedSupply + assignedRescue;
        if (totalAssigned > 0) {
            std::cout << "Team " << teamId << " assigned "
                    << totalAssigned << " requests ("
                    << assignedSupply << " SUPPLY, "
                    << assignedRescue << " RESCUE), total workload "
                    << team.getCurrentWorkload() << ".\n";  
        }

    return true;
}


bool QuakeAssistController::handleDispatchTeam(int teamId) {
    int idx = findTeamIndexById(teamId);
    if (idx == -1) {
        std::cout << "Error: Invalid team ID.\n" << std::endl;
        return false;
    }
    Team& t = teams[idx];
    if (!t.hasActiveMission()) {
        std::cout << "Error: Team " << teamId << " has no active mission." << std::endl;
        return true;
    }
    int workload = t.getCurrentWorkload();
    std::cout << "Team " << teamId << " dispatched with workload " << workload << "." << std::endl;
    t.clearMission();
    return true;
}

void QuakeAssistController::printQueues() const {
    //Print queues.
    
    Request* supplyData   = supplyQueue.getData();
    int supplyCount = supplyQueue.getCount();
    int supplyCapacity = supplyQueue.getCapacity();
    int supplyFront = supplyQueue.getFrontIndex();

    std::cout << "SUPPLY QUEUE:\n";

    for (int i = 0; i < supplyCount; ++i) {
        int idx = (supplyFront + i) % supplyCapacity;
        const Request& r = supplyData[idx];

        // Örnek format: S101 ANKARA WATER 40 4
        // Tipine göre farklı alanlar yazılabilir
        if (r.getType() == "SUPPLY") {
            std::cout << r.getId()      << " "
                      << r.getCity()    << " "
                      << r.getSupplyType() << " "
                      << r.getAmount()  << " "
                      << r.getEmergencyLevel()
                      << "\n";
        } else { 
            std::cout << r.getId()   << " "
                      << r.getCity() << " "
                      << r.getType() << " "
                      << r.getEmergencyLevel()
                      << "\n";
        }
    }

    std::cout << "RESCUE QUEUE:\n";

    Request* rData   = rescueQueue.getData();
    int      rFront  = rescueQueue.getFrontIndex();
    int      rCount  = rescueQueue.getCount();
    int      rCap    = rescueQueue.getCapacity();

    for (int i = 0; i < rCount; ++i) {
        int idx = (rFront + i) % rCap;
        const Request& r = rData[idx];

        if (r.getType() == "RESCUE") {
            std::cout << r.getId()        << " "
                      << r.getCity()      << " "
                      << r.getNumPeople() << " "
                      << r.getRisk()      << " "
                      << r.getEmergencyLevel()
                      << "\n";
        } else { 
            std::cout << r.getId()   << " "
                      << r.getCity() << " "
                      << r.getType() << " "
                      << r.getEmergencyLevel()
                      << "\n";
        }
    }
    

}

void QuakeAssistController::printTeam(int teamId) const {
    //Print team data using teamId.
    int idx = findTeamIndexById(teamId);
    if (idx == -1) {
        std::cout << "Error: Invalid team ID.\n";
        return;
    }

    const Team& team = teams[idx];
    const MissionStack& stack = team.getMissionStack();

    int top = stack.getTopIndex();         
    const Request* data = stack.getData();

    std::cout << "TEAM " << teamId << " STACK:\n";
    
    if (top == -1) return;
    
    
    for (int i = top; i >= 0; --i) {
        const Request& r = data[i];

        if (r.getType() == "SUPPLY") {
            std::cout << r.getId() << " "
                      << r.getCity() << " "
                      << r.getSupplyType() << " "
                      << r.getAmount() << " "
                      << r.getEmergencyLevel()
                      << "\n";
        } else { // RESCUE
            std::cout << r.getId() << " "
                      << r.getCity() << " "
                      << r.getNumPeople() << " "
                      << r.getRisk() << " "
                      << r.getEmergencyLevel()
                      << "\n";
        }
    }
}

void QuakeAssistController::clear() {
    //Clear data.
    supplyQueue.clear();
    rescueQueue.clear();
    for (int i = 0; i < teamCount; ++i) {
        teams[i].clearMission();   // ya da teams[i].getMissionStack().clear();
    }

}
