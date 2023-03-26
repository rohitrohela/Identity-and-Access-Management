/* @TODO replace with your variables
 * ensure all variables on this page match your project
 */

export const environment = {
  production: false,
  apiServerUrl: 'http://127.0.0.1:5000', // the running FLASK api server url
  auth0: {
    url: 'fsndrr.us', // the auth0 domain prefix
    audience: 'coffee-shop', // the audience set for the auth0 app
    clientId: '5e1zcS7la5qizoQ1jcqqYeI1nU0bbZin', // the client id generated for the auth0 app
    callbackURL: 'http://localhost:8100', //  (my Auth0 serer allowed callback URL : http://localhost:8100/tabs/user-page)
  }
};
