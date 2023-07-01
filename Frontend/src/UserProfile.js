import { ReactSession } from 'react-client-session';
ReactSession.setStoreType("localStorage");
var UserProfile = (function() {
    var full_name = "";
    var id = -1;
    var getName = function() {
      return full_name;   
    };
    
    var setName = function(name) {
      full_name = name;     
    };
    var getId = function(){
      return id;
    };
    var setId = function(new_id){
      id=new_id;
    };
    var getUsername = function(){
        return ReactSession.get("username") === "" ? undefined : ReactSession.get("username");
    };
    var setUsername = function(username){
        ReactSession.set("username",username);
    };
    var Reset = function(){
      full_name = undefined;
      id = undefined;
      setUsername(undefined);
    };
    return {
      getName: getName,
      setName: setName,
      setUsername: setUsername,
      getUsername: getUsername,
      getId: getId,
      setId: setId,
      Reset: Reset,
    };
  
  })();
  
  export default UserProfile;