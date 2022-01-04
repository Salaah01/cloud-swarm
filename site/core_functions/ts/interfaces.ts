/**Shared interfaces. */

export interface ConnectState {
  [key: string]: any;
}

/**Interface for an action with unknown properties. */
export interface anyPropsObj {
  [key: string]: any;
}

/**Interface for a reducer. */
export interface reducerAction {
  type: string;
  [x: string]: any;
}

// Model Interfaces