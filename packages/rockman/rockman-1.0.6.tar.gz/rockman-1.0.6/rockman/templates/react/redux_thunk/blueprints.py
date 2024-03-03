
action_template = """
import { Dispatch } from 'redux';
import { {model_name_capitalize}ActionTypes, {model_name_capitalize}Request, {model_name_capitalize}Response, {model_name_capitalize}Error } from '../types/{model_name}_types';
import axios, { AxiosError, AxiosResponse } from "axios";
axios.defaults.withCredentials = true;
// [ANCHOR_1]
    """

reducer_template = """
import { {model_name_capitalize}ActionTypes, {model_name_capitalize}State } from '../types/{model_name}_types';

const initialState: {model_name_capitalize}State = {
    id: "",
    name: '',
    data: [],
    {plural_model_name_lower}: [],
    error: null,
    message: '',
    loading: false,
    deleted: null,
    new_one: null,
    new_ones: [],
};

const {model_name_capitalize}Reducer = (state = initialState, action: {model_name_capitalize}ActionTypes) => {
    switch (action.type) {
// [ANCHOR_1]
        case 'START_LOADING':
            return {...state, loading: true};
        case 'END_LOADING':
            return {...state, loading: false};
        default:
            return state;
    }
};

export default {model_name_capitalize}Reducer;
    """

types_template = """
export interface {model_name_capitalize} {
    id: string;
    name: string;
}

export interface {model_name_capitalize}Request {
    id: string;
    name: string;
    fk_id?: string;
    error?: any;
    message?: string;
}

export interface {model_name_capitalize}Error {
    id: [string];
    name: [string];
}

export interface {model_name_capitalize}Response {
    id: string;
    name: string;
    data: {model_name_capitalize}Request[];
    error?: {model_name_capitalize}Error | null;
    message?: string;
    loading?: boolean;
    deleted?: {model_name_capitalize}Request | null;
    new_one?: {model_name_capitalize}Request | null;
    new_ones?: {model_name_capitalize}Request[];
    {plural_model_name_lower}?: {model_name_capitalize}Request[];
}

export type {model_name_capitalize}State = {model_name_capitalize}Response;

export const START_LOADING = 'START_LOADING';
export const END_LOADING = 'END_LOADING';
// [ANCHOR_1]

interface StartLoadingAction {
type: typeof START_LOADING;
payload: {model_name_capitalize}Request;
}

interface EndLoadingAction {
type: typeof END_LOADING;
payload: {model_name_capitalize}Request;
}
// [ANCHOR_2]

export type {model_name_capitalize}ActionTypes = 
StartLoadingAction
| EndLoadingAction
// [ANCHOR_3]
    """
