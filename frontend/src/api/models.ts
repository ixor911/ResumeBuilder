export type ApiId = number | string;
export type ISODate = string;
export type ISODateTime = string;
export type QueryParams = Record<
  string,
  string | number | boolean | null | undefined
>;

export type AuthTokens = {
  access: string;
  refresh: string;
};

export type User = {
  id: number;
  username: string;
  email: string;
};

export type AuthResponse = AuthTokens & {
  user: User;
};

export type RegisterPayload = {
  username: string;
  email?: string;
  password: string;
};

export type LoginPayload = {
  username: string;
  password: string;
};

export type ResumeProfile = {
  id: number;
  first_name: string;
  last_name: string;
  job_title: string;
  email: string;
  phone: string;
  country: string;
  city: string;
  avatar: string | null;
  created_at: ISODateTime;
  updated_at: ISODateTime;
};

export type ResumeProfileWrite = Partial<
  Omit<ResumeProfile, "id" | "created_at" | "updated_at">
>;

export type SectionType =
  | "summary"
  | "experience"
  | "education"
  | "projects"
  | "skills"
  | "languages"
  | "links"
  | "certificates"
  | "custom";

export type SectionPlacement = "main" | "sidebar";

export type ResumeListItem = {
  id: number;
  owner: string;
  title: string;
  slug: string;
  language: string;
  is_public: boolean;
  is_featured: boolean;
  profile: ResumeProfile | null;
  created_at: ISODateTime;
  updated_at: ISODateTime;
};

export type ResumeWritePayload = {
  title?: string;
  language?: string;
  is_public?: boolean;
  profile?: ResumeProfileWrite;
};

export type ResumeWriteResponse = Omit<ResumeListItem, "owner">;

export type SectionItemBase = {
  id: number;
  section: number;
  order: number;
  is_visible: boolean;
  created_at: ISODateTime;
  updated_at: ISODateTime;
};

export type SummaryItem = SectionItemBase & {
  text: string;
};

export type ExperienceItem = SectionItemBase & {
  position: string;
  company: string;
  location: string;
  employment_type: string;
  start_date: ISODate | null;
  end_date: ISODate | null;
  is_current: boolean;
  description: string;
};

export type EducationItem = SectionItemBase & {
  institution: string;
  degree: string;
  field_of_study: string;
  location: string;
  start_date: ISODate | null;
  end_date: ISODate | null;
  is_current: boolean;
  description: string;
};

export type ProjectItem = SectionItemBase & {
  title: string;
  role: string;
  description: string;
  url: string;
  start_date: ISODate | null;
  end_date: ISODate | null;
  is_featured: boolean;
  tech_stack: string;
};

export type SkillItem = SectionItemBase & {
  name: string;
  category: string;
  level: number | null;
  description: string;
};

export type LanguageItem = SectionItemBase & {
  name: string;
  proficiency: string;
};

export type LinkItem = SectionItemBase & {
  label: string;
  url: string;
  icon: string;
};

export type CertificateItem = SectionItemBase & {
  title: string;
  issuer: string;
  issue_date: ISODate | null;
  expiration_date: ISODate | null;
  credential_id: string;
  url: string;
};

export type SectionItem =
  | SummaryItem
  | ExperienceItem
  | EducationItem
  | ProjectItem
  | SkillItem
  | LanguageItem
  | LinkItem
  | CertificateItem;

export type ResumeSection = {
  id: number;
  resume: number;
  type: SectionType;
  placement: SectionPlacement;
  title: string;
  order: number;
  is_visible: boolean;
  is_locked: boolean;
  created_at: ISODateTime;
  updated_at: ISODateTime;
  items?: SectionItem[];
};

export type ResumeSectionWritePayload = Partial<
  Omit<ResumeSection, "id" | "created_at" | "updated_at" | "items">
> & {
  resume: number;
  type: SectionType;
};

export type ResumeDetail = ResumeListItem & {
  sections: ResumeSection[];
};

export type SectionItemWritePayload<TItem extends SectionItem> = Partial<
  Omit<TItem, "id" | "created_at" | "updated_at">
> & {
  section: number;
};

export type ResumeListParams = QueryParams & {
  search?: string;
  featured?: boolean;
  mine?: boolean;
};
