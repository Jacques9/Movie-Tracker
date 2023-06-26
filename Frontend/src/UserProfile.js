import { ReactSession } from 'react-client-session';
ReactSession.setStoreType("localStorage");
var UserProfile = (function() {
    var full_name = "";
  
    var getName = function() {
      return full_name;    // Or pull this from cookie/localStorage
    };
  
    var setName = function(name) {
      full_name = name;     
      // Also set this in cookie/localStorage
    };
    var getUsername = function(){
        return ReactSession.get("username") === "" ? undefined : ReactSession.get("username");
    }
    var setUsername = function(username){
        ReactSession.set("username",username);
    }
    return {
      getName: getName,
      setName: setName,
      setUsername: setUsername,
      getUsername: getUsername
    }
  
  })();
  
  export default UserProfile;