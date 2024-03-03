
action_method_upload_template = """
export const {model_name_capitalize}{method_name_capitalize} =
  (data: {model_name_capitalize}Request, files: File[]) =>
  async (dispatch: Dispatch<{model_name_capitalize}ActionTypes>) => {
    dispatch({
      type: "START_LOADING",
      payload: { ...data, error: null, message: "START_LOADING" },
    });

    const formData = new FormData();
    formData.append("fk_id", data.fk_id ? data.fk_id.toString() : "");
    files.forEach((file) => {
      formData.append("name", file.name);
      formData.append("files", file);
    });

    axios.post(`${process.env.REACT_APP_API_URL}{prefix}{enpoint_name}/{model_name_for_url}/`, formData, {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      })
      .then((response: AxiosResponse<{model_name_capitalize}Response>) => {
        dispatch({ type: "{model_name_upper}_{method_name_upper}_{method_name_upper}", payload: response.data });

        setTimeout(() => {
          dispatch({
            type: "{model_name_upper}_{method_name_upper}_SUCCESS",
            payload: {
              ...response.data,
              error: null,
              message: "{method_name_upper}_SUCCESS",
            },
          });
        }, 3000);

        dispatch({
          type: "END_LOADING",
          payload: { ...data, error: null, message: "END_LOADING" },
        });
      })
      .catch((error: AxiosError<{model_name_capitalize}Error>) => {
        if (error.response) {
          dispatch({
            type: "{model_name_upper}_{method_name_upper}_FAIL",
            payload: error.response.data,
          });
          dispatch({
            type: "END_LOADING",
            payload: { ...data, error: null, message: "END_LOADING" },
          });
        } else if (error.request) {
          console.log("No response received:", error.request);
        } else {
          console.log("Error:", error.message);
        }
      });
  };
// [ANCHOR_1]
"""

action_method_query_template = """
export const {model_name_capitalize}{method_name_capitalize} =
  (data: {model_name_capitalize}Request) =>
  async (dispatch: Dispatch<{model_name_capitalize}ActionTypes>) => {
    dispatch({
      type: "START_LOADING",
      payload: { ...data, error: null, message: "START_LOADING" },
    });

    axios.get(`${process.env.REACT_APP_API_URL}{prefix}{api_name}/{model_name_url}?id=${data.fk_id}&name=${data.name}`)
      .then((response: AxiosResponse<{model_name_capitalize}Response>) => {
        dispatch({ type: "{model_name_upper}_{method_name_upper}", payload: response.data });

        dispatch({
        type: "{model_name_upper}_{method_name_upper}_SUCCESS",
        payload: {
            ...response.data,
            error: null,
            message: "{method_name_upper}_SUCCESS",
        },
        });

        dispatch({
          type: "END_LOADING",
          payload: { ...data, error: null, message: "END_LOADING" },
        });
      })
      .catch((error: AxiosError<{model_name_capitalize}Error>) => {
        if (error.response) {
          dispatch({
            type: "{model_name_upper}_{method_name_upper}_FAIL",
            payload: error.response.data,
          });
          dispatch({
            type: "END_LOADING",
            payload: { ...data, error: null, message: "END_LOADING" },
          });
        } else if (error.request) {
          console.log("No response received:", error.request);
        } else {
          console.log("Error:", error.message);
        }
      });
  };
// [ANCHOR_1]
"""

action_method_post_template = """
export const {model_name_capitalize}{method_name_capitalize} =
  (data: {model_name_capitalize}Request) =>
  async (dispatch: Dispatch<{model_name_capitalize}ActionTypes>) => {
    dispatch({
      type: "START_LOADING",
      payload: { ...data, error: null, message: "START_LOADING" },
    });

    
    axios.post(`${process.env.REACT_APP_API_URL}{prefix}{api_name}/{model_name_url}/`, data)
      .then((response: AxiosResponse<{model_name_capitalize}Response>) => {
        dispatch({ type: "{model_name_upper}_{method_name_upper}", payload: response.data });

        dispatch({
        type: "{model_name_upper}_{method_name_upper}_SUCCESS",
        payload: {
            ...response.data,
            error: null,
            message: "{method_name_upper}_SUCCESS",
        },
        });

        dispatch({
          type: "END_LOADING",
          payload: { ...data, error: null, message: "END_LOADING" },
        });
      })
      .catch((error: AxiosError<{model_name_capitalize}Error>) => {
        if (error.response) {
          dispatch({
            type: "{model_name_upper}_{method_name_upper}_FAIL",
            payload: error.response.data,
          });
          dispatch({
            type: "END_LOADING",
            payload: { ...data, error: null, message: "END_LOADING" },
          });
        } else if (error.request) {
          console.log("No response received:", error.request);
        } else {
          console.log("Error:", error.message);
        }
      });
  };
// [ANCHOR_1]
"""

action_method_get_template = """
export const {model_name_capitalize}{method_name_capitalize} =
  (data: {model_name_capitalize}Request) =>
  async (dispatch: Dispatch<{model_name_capitalize}ActionTypes>) => {
    dispatch({
      type: "START_LOADING",
      payload: { ...data, error: null, message: "START_LOADING" },
    });

    axios.get(`${process.env.REACT_APP_API_URL}{prefix}{api_name}/{model_name_url}?id=${data.fk_id}&name=${data.name}`)
      .then((response: AxiosResponse<{model_name_capitalize}Response>) => {
        dispatch({ type: "{model_name_upper}_{method_name_upper}", payload: response.data });

        dispatch({
        type: "{model_name_upper}_{method_name_upper}_SUCCESS",
        payload: {
            ...response.data,
            error: null,
            message: "{method_name_upper}_SUCCESS",
        },
        });

        dispatch({
          type: "END_LOADING",
          payload: { ...data, error: null, message: "END_LOADING" },
        });
      })
      .catch((error: AxiosError<{model_name_capitalize}Error>) => {
        if (error.response) {
          dispatch({
            type: "{model_name_upper}_{method_name_upper}_FAIL",
            payload: error.response.data,
          });
          dispatch({
            type: "END_LOADING",
            payload: { ...data, error: null, message: "END_LOADING" },
          });
        } else if (error.request) {
          console.log("No response received:", error.request);
        } else {
          console.log("Error:", error.message);
        }
      });
  };
// [ANCHOR_1]
"""

action_method_put_template = """
export const {model_name_capitalize}{method_name_capitalize} =
  (data: {model_name_capitalize}Request) =>
  async (dispatch: Dispatch<{model_name_capitalize}ActionTypes>) => {
    dispatch({
      type: "START_LOADING",
      payload: { ...data, error: null, message: "START_LOADING" },
    });

    axios.put(`${process.env.REACT_APP_API_URL}{prefix}{api_name}/{model_name_url}/`, data)
      .then((response: AxiosResponse<{model_name_capitalize}Response>) => {
        dispatch({ type: "{model_name_upper}_{method_name_upper}", payload: response.data });

        dispatch({
        type: "{model_name_upper}_{method_name_upper}_SUCCESS",
        payload: {
            ...response.data,
            error: null,
            message: "{method_name_upper}_SUCCESS",
        },
        });

        dispatch({
          type: "END_LOADING",
          payload: { ...data, error: null, message: "END_LOADING" },
        });
      })
      .catch((error: AxiosError<{model_name_capitalize}Error>) => {
        if (error.response) {
          dispatch({
            type: "{model_name_upper}_{method_name_upper}_FAIL",
            payload: error.response.data,
          });
          dispatch({
            type: "END_LOADING",
            payload: { ...data, error: null, message: "END_LOADING" },
          });
        } else if (error.request) {
          console.log("No response received:", error.request);
        } else {
          console.log("Error:", error.message);
        }
      });
  };
// [ANCHOR_1]
"""
action_method_delete_template = """
export const {model_name_capitalize}{method_name_capitalize} =
  (data: {model_name_capitalize}Request) =>
  async (dispatch: Dispatch<{model_name_capitalize}ActionTypes>) => {
    dispatch({
      type: "START_LOADING",
      payload: { ...data, error: null, message: "START_LOADING" },
    });

    axios.delete(`${process.env.REACT_APP_API_URL}{prefix}{api_name}/{model_name_url}?id=${data.fk_id}&name=${data.name}`)
      .then((response: AxiosResponse<{model_name_capitalize}Response>) => {
        dispatch({ type: "{model_name_upper}_{method_name_upper}", payload: response.data });

        dispatch({
        type: "{model_name_upper}_{method_name_upper}_SUCCESS",
        payload: {
            ...response.data,
            error: null,
            message: "{method_name_upper}_SUCCESS",
        },
        });

        dispatch({
          type: "END_LOADING",
          payload: { ...data, error: null, message: "END_LOADING" },
        });
      })
      .catch((error: AxiosError<{model_name_capitalize}Error>) => {
        if (error.response) {
          dispatch({
            type: "{model_name_upper}_{method_name_upper}_FAIL",
            payload: error.response.data,
          });
          dispatch({
            type: "END_LOADING",
            payload: { ...data, error: null, message: "END_LOADING" },
          });
        } else if (error.request) {
          console.log("No response received:", error.request);
        } else {
          console.log("Error:", error.message);
        }
      });
  };
// [ANCHOR_1]
"""