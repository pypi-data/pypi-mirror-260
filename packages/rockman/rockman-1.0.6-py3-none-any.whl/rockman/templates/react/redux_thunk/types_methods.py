default_type_template_anchor_1 = """
export const {model_name_upper}_{method_name_upper} = '{model_name_upper}_{method_name_upper}';
export const {model_name_upper}_{method_name_upper}_SUCCESS = '{model_name_upper}_{method_name_upper}_SUCCESS';
export const {model_name_upper}_{method_name_upper}_FAIL = '{model_name_upper}_{method_name_upper}_FAIL';
// [ANCHOR_1]
"""

default_type_template_anchor_2 = """
interface {model_name_capitalize}{method_name_capitalize}Action {
type: typeof {model_name_upper}_{method_name_upper};
payload: {model_name_capitalize}Response;
}
interface {model_name_capitalize}{method_name_capitalize}SuccessAction {
type: typeof {model_name_upper}_{method_name_upper}_SUCCESS;
payload: {model_name_capitalize}Response;
}
interface {model_name_capitalize}{method_name_capitalize}ErrorAction {
type: typeof {model_name_upper}_{method_name_upper}_FAIL;
payload: {model_name_capitalize}Error;
}
// [ANCHOR_2]
"""

default_type_template_anchor_3 = """
| {model_name_capitalize}{method_name_capitalize}Action 
| {model_name_capitalize}{method_name_capitalize}SuccessAction 
| {model_name_capitalize}{method_name_capitalize}ErrorAction 
// [ANCHOR_3]
"""