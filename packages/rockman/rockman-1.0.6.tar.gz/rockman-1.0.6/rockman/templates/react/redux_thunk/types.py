default_type_template_anchor_1 = """
export const {method_name_upper} = '{method_name_upper}';
export const {method_name_upper}_SUCCESS = '{method_name_upper}_SUCCESS';
export const {method_name_upper}_FAIL = '{method_name_upper}_FAIL';"""

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
// [ANCHOR_2]"""

default_type_template_anchor_3 = """
| {model_name_capitalize}{method_name_capitalize}Action 
| {model_name_capitalize}{method_name_capitalize}SuccessAction 
| {model_name_capitalize}{method_name_capitalize}ErrorAction 
// [ANCHOR_3]"""