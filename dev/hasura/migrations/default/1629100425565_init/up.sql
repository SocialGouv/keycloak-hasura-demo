SET check_function_bodies = false;
CREATE TABLE public.books (
    id integer NOT NULL,
    name text NOT NULL,
    creator_id text NOT NULL,
    publication_date text
);
CREATE SEQUENCE public.book_id_seq
    AS integer
    START WITH 1
    INCREMENT BY 1
    NO MINVALUE
    NO MAXVALUE
    CACHE 1;
ALTER SEQUENCE public.book_id_seq OWNED BY public.books.id;
CREATE TABLE public."user" (
    id text NOT NULL,
    email text NOT NULL,
    first_name text,
    username text,
    last_name text
);
ALTER TABLE ONLY public.books ALTER COLUMN id SET DEFAULT nextval('public.book_id_seq'::regclass);
ALTER TABLE ONLY public.books
    ADD CONSTRAINT book_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public."user"
    ADD CONSTRAINT user_pkey PRIMARY KEY (id);
ALTER TABLE ONLY public.books
    ADD CONSTRAINT books_author_fkey FOREIGN KEY (creator_id) REFERENCES public."user"(id) ON UPDATE RESTRICT ON DELETE RESTRICT;
