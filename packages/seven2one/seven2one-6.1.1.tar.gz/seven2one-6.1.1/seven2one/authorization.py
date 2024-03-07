from uuid import uuid4
import pandas as pd
from loguru import logger

from .utils.ut import Utils
from .utils.ut_auth import AuthData

class Authorization:


    def __init__(self, endpoint:str, client:object, auth_data: AuthData) -> None:
        self.client = client

        self.raiseException = client.raiseException
        self.defaults = client.defaults

        self.auth_data = auth_data
        self.endpoint = endpoint
        self.proxies = client.proxies
        self.structure = client.structure
        self.scheme = client.scheme

    def getVersion(self):
        """
        Returns name and version of the responsible micro service
        """

        return Utils._getServiceVersion(self, 'authorization')

    def _resolve_where(self, where:str):
        resolvedFilter = ''
        if where != None: 
            resolvedFilter = f'({Utils._resolveWhere(self, where)["topLevel"]})'
        
        return resolvedFilter

    def roles(
        self, 
        fields:list=None,
        where:str=None
        ) -> pd.DataFrame:
        """
        Returns a DataFrame of available roles
        """

        key = 'roles'

        if fields != None:
            if type(fields) != list:
                fields = [fields]
            _fields = Utils._queryFields(fields, recursive=True)   
        else:
            _fields =f'''
                id
                name
                revision
            ''' 

        resolvedFilter = self._resolve_where(where)
        graphQLString = f'''query roles {{
            {key}{resolvedFilter}  {{
                {_fields}
            }}
        }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        df = pd.json_normalize(result[key])
        return df

    def rules(
        self,
        fields:list=None, 
        where:str=None
        ) -> pd.DataFrame:
        """
        Returns a DataFrame of available rules
        """

        key = 'rules'

        if fields != None:
            if type(fields) != list:
                fields = [fields]
            _fields = Utils._queryFields(fields, recursive=True)   
        else:
            _fields =f'''
                id
                filter
                revision
                role {{
                    id
                    name
                }}
                accountReference {{
                    ...on GroupReference {{
                        group {{
                            id
                            name
                        }}
                    }}
                    ...on ServiceAccountReference {{
                        serviceAccount {{
                            id
                            name
                        }}
                    }}
                }}
            ''' 

        resolvedFilter = self._resolve_where(where)
        graphQLString = f'''query Rules {{
            {key}{resolvedFilter}  {{
                {_fields}
            }}
        }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        df = pd.json_normalize(result[key])
        return df

    def users(
        self,
        fields:list=None, 
        where:str=None) -> pd.DataFrame:
        """
        Returns a DataFrame of available users
        """

        key = 'users'

        if fields != None:
            if type(fields) != list:
                fields = [fields]
            _fields = Utils._queryFields(fields, recursive=True)   
        else:
            _fields =f'''
                id
                userId
                username
                eMail
                providerUserId
                isServiceAccount  
            ''' 

        resolvedFilter = self._resolve_where(where)
        graphQLString = f'''query Users {{
            {key}{resolvedFilter}  {{
                {_fields}
            }}
        }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        df = pd.json_normalize(result[key])
        return df

    def userGroups(
        self,
        fields:list=None, 
        where:str=None
        ) -> pd.DataFrame:
        """
        Returns a DataFrame of available users
        """

        key = 'groups'

        if fields != None:
            if type(fields) != list:
                fields = [fields]
            _fields = Utils._queryFields(fields, recursive=True)   
        else:
            _fields =f'''
                id
                name
            ''' 

        resolvedFilter = self._resolve_where(where)
        graphQLString = f'''query Groups {{
            {key}{resolvedFilter}  {{
                {_fields}
            }}
        }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        df = pd.json_normalize(result[key])
        return df

    def serviceAccounts(
        self,
        fields:list=None, 
        where:str=None
        ) -> pd.DataFrame:
        """
        Returns a DataFrame of available service accounts.
        """

        key = 'serviceAccounts'

        if fields != None:
            if type(fields) != list:
                fields = [fields]
            _fields = Utils._queryFields(fields, recursive=True)   
        else:
            _fields =f'''
                id
                name
            ''' 

        resolvedFilter = self._resolve_where(where)
        graphQLString = f'''query ServiceAccounts {{
            {key}{resolvedFilter}  {{
                {_fields}
            }}
        }}
        '''

        result = Utils._executeGraphQL(self, graphQLString)
        if result == None: return

        df = pd.json_normalize(result[key])
        return df

    def createRole(
        self,
        inventoryName:str, 
        roleName:str,
        userGroups:list=None, 
        objectPermissions:list=['Create', 'Delete'], 
        propertiesPermissions:list=['Read', 'Update']
        ) -> None:

        """
        Creates a role and sets all rights to all properties

        Parameters:
        ----------
        inventoryName : str
            The name of the inventory for which the new role authorizes rights.
        roleName : str
            Name of the new role.
        userGroup : list = None
            List of user group names. If None, the role will be created without attaching user groups.
        objectPermissions : list = ['Create', 'Delete']
            Default is 'Create' and 'Delete' to allow creating and deleting items of the specified inventory.
            Other entries are not allowed.
        propertiesPermissions : list = ['Read', 'Update']
            Default is 'Read' and 'Update'. All properties will receive 
            the specified rights. Other entries are not allowed.
            Permissions are not extended on referenced inventories!
        """

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):

            # Parameter validation
            try:
                self.client.structure[inventoryName]
            except:
                Utils._error(self, f"Unknown inventory '{inventoryName}'")
                return
            
            try:
                roles = self.roles()
                if roleName in list(roles['name']):
                    Utils._error(self, f"Role '{roleName}' already exists.")
                    return
            except:
                pass

            if isinstance(userGroups, str):
                userGroups = [userGroups]

            if userGroups != None:
                # 'in' is not supported therefore load all groups
                dfUserGroups = self.userGroups()
                falseUserGroups = []
                for group in userGroups:
                    if group not in list(dfUserGroups['name']):
                        falseUserGroups.append(group)
                
                if falseUserGroups:
                    Utils._error(self, f"Unknown user group(s) {falseUserGroups}")
                    return

            # Create role
            properties = self.client.structure[inventoryName]['properties']

            ppstring = '[' + ','.join(map(str.upper, propertiesPermissions)) + ']'
            props = '[\n'
            refProps = '[\n'
            for _, value in properties.items():
                if value["type"] == 'scalar':
                    props += f'{{ propertyId: {Utils._toGraphQL(value["propertyId"])}\n permissions: {ppstring} }}\n'
                elif value["type"] == 'reference':
                    refProps += f'{{ propertyId: {Utils._toGraphQL(value["propertyId"])}\n inventoryId: {Utils._toGraphQL(value["inventoryId"])}\n propertyPermissions: {ppstring}\n inventoryPermissions: [NONE]\n properties: []\n referencedProperties: []\n }}'
            props += ']'
            refProps += ']'
            
            graphQLString= f'''
            mutation AddRole($roleName: String!, $inventoryId: String!, $inventoryPermissions: [ObjectPermission!]!) {{ 
                addRoles (input: {{
                    roles: {{
                        name: $roleName
                        rootInventoryPermission: {{
                            inventoryId: $inventoryId
                            inventoryPermissions: $inventoryPermissions
                            properties: {props}
                            referencedProperties: {refProps}
                            }}
                        }}
                    }})
                    {{
                    roles {{
                        id
                    }}
                }}
            }}
            '''
            params = {
                "roleName": roleName,
                "inventoryId": self.client.structure[inventoryName]['inventoryId'],
                "inventoryPermissions": list(map(str.upper, objectPermissions)),
            }

            result = Utils._executeGraphQL(self, graphQLString, correlationId, params=params)
            if result == None: return

            # if result['addRole']['errors']:
            #     Utils._listGraphQlErrors(result, 'createInventory')
            #     return

            logger.info(f"Role {roleName} created.")

            roleId = result['addRoles']['roles'][0]['id']

            # Create rules
            if userGroups != None:
                for groupname in userGroups:
                    groupId = dfUserGroups.set_index('name').to_dict(orient='index')[groupname]['id']
                    createRuleGqlString= f'''
                    mutation AddRule($roleId: String!, $groupId: String!) {{
                        addRules (input: {{
                            rules: {{
                                roleId: $roleId
                                groupId: $groupId
                                filter: ""
                                filterFormat: EXPRESSION
                                }}
                            }})
                            {{
                            rules {{
                                ruleId
                            }}
                        }}
                    }}
                    '''
                    result = Utils._executeGraphQL(self, createRuleGqlString, correlationId, params={"roleId": roleId, "groupId": groupId})
                    if result != None:
                        logger.info(f"Rule for {roleName} and user group {group} created.")
                    else:
                        logger.error(f"Rule for {roleName} and user group {group} could not be created.")

            return

    def deleteRole(self, role:str) -> None:
        """
        Deletes a role and all related rules.
        """

        correlationId = str(uuid4())
        with logger.contextualize(correlation_id=correlationId):

            # Get Ids of roles and rules
            roles = self.roles().set_index('name')
            roleId = roles.loc[role,'id']

            rules = self.rules()
            rules = rules.set_index('role.name')
            try:
                ruleIds = rules.loc[role,'id']
            except:
                ruleIds = []
            if not isinstance(ruleIds, str):
                ruleIds = list(ruleIds)
            else:
                ruleIds = [ruleIds]

            # First delete rules
            if ruleIds:
                deleteRuleGraphQLString = f'''
                mutation deleteRule($ruleId: String!) {{
                    removeRule(input: {{
                        ruleId: $ruleId
                    }}) {{
                        ruleId
                    }}
                }}
                '''
                for ruleId in ruleIds:
                    result = Utils._executeGraphQL(self, deleteRuleGraphQLString, correlationId, {"ruleId": ruleId})
                    if result != None:
                        logger.info(f"Rule {ruleId} of role {role} with id {ruleId} has been deleted.")
                    else:
                        Utils._error(self, f"Rule {ruleId} of role {roleId} could not be deleted.")
                        return

            # After all rules have been deleted, delete the role
            deleteRoleGraphQLString = f'''
            mutation deleteRole($roleId: String!) {{
                removeRole(input: {{
                    roleId: $roleId
                }}) {{
                    roleId
                }}
            }}
            '''
            result = Utils._executeGraphQL(self, deleteRoleGraphQLString, correlationId, {"roleId": roleId})
            if result != None:
                logger.info(f"Role {role} with id {roleId} has been deleted.")
            else:
                Utils._error(self, f"Role {roleId} could not be deleted.")
            
            return

    def addRule(self, role:str, group:str):
        """
        Adds a rule connecting role with usergroup.
        """

        roleId = self.roles(fields=['id'], where=f'name eq "{role}"')['id'][0]
        groupId = self.userGroups(fields=['id'], where=f'name eq "{group}"')['id'][0]

        graphqlString= f'''
        mutation AddRule($roleId: String!, $groupId: String!) {{
            addRules (input: {{
                rules: {{
                    roleId: $roleId
                    groupId: $groupId
                    filter: ""
                    filterFormat: EXPRESSION
                    }}
                }})
                {{
                rules {{
                    ruleId
                }}
            }}
        }}
        '''
        logger.debug(graphqlString)
        params = {
            "roleId": roleId,
            "groupId": groupId
        }
        result = Utils._executeGraphQL(self, graphqlString, params=params)
        if result != None:
            logger.info(f"Rule for {role} and user group {groupId} created.")
        else:
            Utils._error(self, f"Rule could not be created.")

        return
