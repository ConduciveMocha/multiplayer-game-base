import { flaskServer } from "../constants/urls";

export function decodeJwt(jwt) {
  let base64Url = jwt.split(".")[1];
  let base64 = base64Url.replace("-", "+").replace("_", "/");
  let decoded = JSON.parse(window.atob(base64));

  return decoded;
}
export async function jsonPost(payload, route) {
  const resp = await fetch(flaskServer + route, {
    method: "POST",
    mode: "cors",
    headers: {
      "Content-Type": "application/json",
      cache: "no-cache"
    },
    credentials: "same-origin",
    redirect: "follow",
    body: JSON.stringify(payload)
  });
  const resp_json = await resp.json();
  return resp_json;
}

export function setAuthCookie(resp) {
  if (resp.auth) {
    const decoded_jwt = decodeJwt(resp.auth);
    document.cookie = `auth=${resp.auth}; max-age=${decoded_jwt.exp -
      decoded_jwt.iat}`;
    return decoded_jwt;
  } else throw new Error("JWT not returned in response");
}

export function getAuthCookie() {
  return document.cookie.replace(
    /(?:(?:^|.*;\s*)auth\s*\=\s*([^;]*).*$)|^.*$/,
    "$1"
  );
}

export function appendJwt(payload) {
  return { ...payload, auth: getAuthCookie() };
}

export const withJwt = f =>
  async function() {
    arguments[0] = { ...arguments[0], auth: getAuthCookie() };
    const request_resp = await f.apply(this, arguments);
    try {
      const decoded_jwt = setAuthCookie(request_resp);
      return { resp: request_resp, jwt: decoded_jwt };
    } catch (error) {
      return { resp: request_resp, error: error };
    }
  };

export const submitLogin = (username, password) =>
  withJwt(jsonPost)({ username: username, password: password }, "/auth/login");

export const submitRegistration = registrationFrom =>
  jsonPost(registrationFrom);
