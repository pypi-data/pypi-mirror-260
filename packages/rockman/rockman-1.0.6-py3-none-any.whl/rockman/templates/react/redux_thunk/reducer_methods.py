default_reducer_template = """
        case '{model_name_upper}_{method_name_upper}':
            return {...state, {plural_model_name_lower}: action.payload.{plural_model_name_lower}, error: null, message: action.payload.message};
        case '{model_name_upper}_{method_name_upper}_SUCCESS':
            return {...state, error: null, message: action.payload.message};
        case '{model_name_upper}_{method_name_upper}_FAIL':
            return {...state, error: action.payload, message: '{method_name_upper}_FAIL'};
// [ANCHOR_1]
"""

upload_reducer_template = """
        case '{model_name_upper}_{method_name_upper}':
            return {...state, {plural_model_name_lower}: action.payload.{plural_model_name_lower}, error: null, message: action.payload.message};
        case '{model_name_upper}_{method_name_upper}_SUCCESS':
            return {...state, error: null, message: action.payload.message};
        case '{model_name_upper}_{method_name_upper}_FAIL':
            return {...state, error: action.payload, message: '{method_name_upper}_FAIL'};
// [ANCHOR_1]
"""