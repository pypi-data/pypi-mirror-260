import { Globals, SN_FILE_LIBRARY_URL, SN_V2_FILE_LIBRARY_URL } from './config';
import jwt_decode from 'jwt-decode';

export class SkillsNetworkFileLibrary {
  #contextPath: string;

  constructor(contextPath: string) {
    this.#contextPath = contextPath;
  }

  launch() {
    const token = Globals.TOKENS.get(this.#contextPath.split('/').pop() || '');
    const token_info = token
      ? (jwt_decode(token) as { [key: string]: any })
      : {};
    const anchor = document.createElement('a');

    if ('project_id' in token_info) {
      anchor.href = `${SN_FILE_LIBRARY_URL}?atlas_token=${token}`;
    } else {
      anchor.href = `${SN_V2_FILE_LIBRARY_URL}?lab_version_id=${token_info.version_id}`;
    }

    anchor.target = '_blank';
    document.body.appendChild(anchor);
    anchor.click();
    document.body.removeChild(anchor);
  }
}
