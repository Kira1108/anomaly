import axios from "axios";
import qs from 'qs'

import { Message } from 'element-ui';

function sendGetRequest(url, data) {
  return new Promise(function (resolve, reject) {
    axios.get(url, {
      headers: {
        // localStorage.getItem('token') ?localStorage.getItem('token') : 
        'token': sessionStorage.getItem('token') ? sessionStorage.getItem('token') : '',
      },
      params: data
    }).then(
      (res) => {
        if (res.status != 200) {
          Message.error(res.data.message);
        }
        resolve(res);
      },
      (err) => {
        reject(err);
      }
    );
  });
}
function sendPostRequest(url, data) {
  // 一个状态为resolve（包裹的是数据）
  // 或者状态为reject （包裹的是错误信息）
  // 的promise对象
  return new Promise(function (resolve, reject) {
    axios.post(url, data, {
      headers: {
        // localStorage.getItem('token') ?localStorage.getItem('token') : 
        'token': sessionStorage.getItem('token') ? sessionStorage.getItem('token') : '',
        'accept': 'application/json',
        'Content-Type': 'application/x-www-form-urlencoded',
        // "Content-Type": "multipart/form-data"
      }
    }).then(
      (res) => {
        if (res.status != 200) {
          Message.error(res.data.message);
        }
        resolve(res);
      },
      (err) => {
        reject(err);
      }
    );
  });
}
function sendPostJSONRequest(url, data) {
  // 一个状态为resolve（包裹的是数据）
  // 或者状态为reject （包裹的是错误信息）
  // 的promise对象
  return new Promise(function (resolve, reject) {
    axios.post(url, data, {
      headers: {
        // localStorage.getItem('token') ?localStorage.getItem('token') : 
        'token': sessionStorage.getItem('token') ? sessionStorage.getItem('token') : '',
        // 'accept': 'application/json',
        // 'Content-Type': 'application/x-www-form-urlencoded',
        "Content-Type": "application/json"
      }
    }).then(
      (res) => {
        if (res.status != 200) {
          Message.error(res.data.message);
        }
        resolve(res);
      },
      (err) => {
        reject(err);
      }
    );
  });
}
function sendPutRequest(url, data) {
  // 一个状态为resolve（包裹的是数据）
  // 或者状态为reject （包裹的是错误信息）
  // 的promise对象
  return new Promise(function (resolve, reject) {
    axios.put(url + (data.id ? data.id : ''), data.data, {
      headers: {
        // localStorage.getItem('token') ?localStorage.getItem('token') : 
        'token': sessionStorage.getItem('token') ? sessionStorage.getItem('token') : ''
      }
    }).then(
      (res) => {
        resolve(res);
      },
      (err) => {
        reject(err);
      }
    );
  });
}

function sendDeleteRequest(url, data) {
  // 一个状态为resolve（包裹的是数据）
  // 或者状态为reject （包裹的是错误信息）
  // 的promise对象
  return new Promise(function (resolve, reject) {
    axios.get(url + data, {
      headers: {
        // localStorage.getItem('token') ?localStorage.getItem('token') : 
        'token': sessionStorage.getItem('token') ? sessionStorage.getItem('token') : ''
      }
    }).then(
      (res) => {
        resolve(res);
      },
      (err) => {
        reject(err);
      }
    );
  });
}

// 接口列表
export default {
  // 首页-------------------------------------
  get() {
    return sendGetRequest("");
  },
  post() {
    return sendPostRequest("");
  },
  put() {
    return sendPutRequest("");
  },
  delete() {
    return sendDeleteRequest("");
  },

  //登录
  postLogin(data) {
    return sendPostRequest('/login', qs.stringify(data))
  },
  //IMAge
  postlimitOffset(data) {
    return sendGetRequest('/anormaly/text/limit-offset', qs.stringify(data))
  },
  postText(data) {
    return sendGetRequest('/anormaly/text', data)
  },
  postWindow(data) {
    return sendGetRequest('/anormaly/window',data)
  },
  postSexImg(data) {
    return sendGetRequest('/anormaly/sex', data)
  },
  //统计接口
  getOcrCountg(data) {
    return sendGetRequest('/anormaly/ocr_count', qs.stringify(data))
  },
  getTextCountg(data) {
    return sendGetRequest('/anormaly/text_count', qs.stringify(data))
  },
  getSexCountg(data) {
    return sendGetRequest('/anormaly/sex_count', qs.stringify(data))
  }, 
  getWindowCountg(data) {
    return sendGetRequest('/anormaly/window_count', qs.stringify(data))
  },
  getImage(data){
    return sendGetRequest('/anormaly/window_count', qs.stringify(data))
  },

  getImgUrl(data) {
    return sendPostJSONRequest('/anormaly/img',data)
  }
};