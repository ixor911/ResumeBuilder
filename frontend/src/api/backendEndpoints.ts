import {
  API_BASE_URL,
  apiConnector,
  clearAuthTokens,
  getAuthTokens,
  setAuthTokens,
} from "./apiConnector";
import type {
  ApiId,
  AuthResponse,
  CertificateItem,
  EducationItem,
  ExperienceItem,
  LanguageItem,
  LinkItem,
  LoginPayload,
  ProjectItem,
  QueryParams,
  RegisterPayload,
  ResumeDetail,
  ResumeListItem,
  ResumeListParams,
  ResumeSection,
  ResumeSectionWritePayload,
  ResumeWritePayload,
  ResumeWriteResponse,
  SectionItemWritePayload,
  SkillItem,
  SummaryItem,
  User,
} from "./models";

function resourcePath(path: string, id?: ApiId) {
  const normalizedPath = path.startsWith("/") ? path : `/${path}`;
  const basePath = normalizedPath.endsWith("/")
    ? normalizedPath
    : `${normalizedPath}/`;

  if (id === undefined) {
    return basePath;
  }

  return `${basePath}${encodeURIComponent(String(id))}/`;
}

function createCrudEndpoint<
  TRead,
  TCreate extends object = Partial<TRead>,
  TUpdate extends object = Partial<TCreate>,
>(path: string) {
  return {
    async list(params?: QueryParams) {
      const response = await apiConnector.get<TRead[]>(resourcePath(path), {
        params,
      });
      return response.data;
    },

    async retrieve(id: ApiId) {
      const response = await apiConnector.get<TRead>(resourcePath(path, id));
      return response.data;
    },

    async create(payload: TCreate) {
      const response = await apiConnector.post<TRead>(resourcePath(path), payload);
      return response.data;
    },

    async update(id: ApiId, payload: TUpdate) {
      const response = await apiConnector.put<TRead>(
        resourcePath(path, id),
        payload,
      );
      return response.data;
    },

    async partialUpdate(id: ApiId, payload: TUpdate) {
      const response = await apiConnector.patch<TRead>(
        resourcePath(path, id),
        payload,
      );
      return response.data;
    },

    async remove(id: ApiId) {
      await apiConnector.delete(resourcePath(path, id));
    },
  };
}

export const backendEndpoints = {
  meta: {
    baseUrl: API_BASE_URL,
  },

  auth: {
    async register(payload: RegisterPayload) {
      const response = await apiConnector.post<AuthResponse>(
        "/auth/register/",
        payload,
      );
      setAuthTokens(response.data);
      return response.data;
    },

    async login(payload: LoginPayload) {
      const response = await apiConnector.post<AuthResponse>("/auth/login/", payload);
      setAuthTokens(response.data);
      return response.data;
    },

    async logout() {
      try {
        await apiConnector.post("/auth/logout/");
      } finally {
        clearAuthTokens();
      }
    },

    async refresh(refreshToken = getAuthTokens()?.refresh) {
      if (!refreshToken) {
        throw new Error("Refresh token is missing.");
      }

      const response = await apiConnector.post<{ access: string; refresh?: string }>(
        "/auth/refresh/",
        { refresh: refreshToken },
      );
      const tokens = {
        access: response.data.access,
        refresh: response.data.refresh ?? refreshToken,
      };
      setAuthTokens(tokens);
      return tokens;
    },

    async me() {
      const response = await apiConnector.get<User>("/auth/me/");
      return response.data;
    },

    async updateMe(payload: Partial<Pick<User, "email">>) {
      const response = await apiConnector.patch<User>("/auth/me/", payload);
      return response.data;
    },
  },

  resumes: {
    async list(params?: ResumeListParams) {
      const response = await apiConnector.get<ResumeListItem[]>("/resumes/", {
        params,
      });
      return response.data;
    },

    async retrieve(slug: string) {
      const response = await apiConnector.get<ResumeDetail>(
        resourcePath("/resumes", slug),
      );
      return response.data;
    },

    async create(payload: ResumeWritePayload) {
      const response = await apiConnector.post<ResumeWriteResponse>(
        "/resumes/",
        payload,
      );
      return response.data;
    },

    async update(slug: string, payload: ResumeWritePayload) {
      const response = await apiConnector.put<ResumeWriteResponse>(
        resourcePath("/resumes", slug),
        payload,
      );
      return response.data;
    },

    async partialUpdate(slug: string, payload: ResumeWritePayload) {
      const response = await apiConnector.patch<ResumeWriteResponse>(
        resourcePath("/resumes", slug),
        payload,
      );
      return response.data;
    },

    async remove(slug: string) {
      await apiConnector.delete(resourcePath("/resumes", slug));
    },
  },

  sections: createCrudEndpoint<
    ResumeSection,
    ResumeSectionWritePayload,
    Partial<ResumeSectionWritePayload>
  >("/sections"),

  summaryItems: createCrudEndpoint<
    SummaryItem,
    SectionItemWritePayload<SummaryItem>
  >("/summary-items"),

  experienceItems: createCrudEndpoint<
    ExperienceItem,
    SectionItemWritePayload<ExperienceItem>
  >("/experience-items"),

  educationItems: createCrudEndpoint<
    EducationItem,
    SectionItemWritePayload<EducationItem>
  >("/education-items"),

  projectItems: createCrudEndpoint<
    ProjectItem,
    SectionItemWritePayload<ProjectItem>
  >("/project-items"),

  skillItems: createCrudEndpoint<SkillItem, SectionItemWritePayload<SkillItem>>(
    "/skill-items",
  ),

  languageItems: createCrudEndpoint<
    LanguageItem,
    SectionItemWritePayload<LanguageItem>
  >("/language-items"),

  linkItems: createCrudEndpoint<LinkItem, SectionItemWritePayload<LinkItem>>(
    "/link-items",
  ),

  certificateItems: createCrudEndpoint<
    CertificateItem,
    SectionItemWritePayload<CertificateItem>
  >("/certificate-items"),
};
