--
-- PostgreSQL database dump
--

-- Dumped from database version 9.5.23
-- Dumped by pg_dump version 13.2

SET statement_timeout = 0;
SET lock_timeout = 0;
SET idle_in_transaction_session_timeout = 0;
SET client_encoding = 'UTF8';
SET standard_conforming_strings = on;
SELECT pg_catalog.set_config('search_path', '', false);
SET check_function_bodies = false;
SET xmloption = content;
SET client_min_messages = warning;
SET row_security = off;

SET default_tablespace = '';

--
-- Name: balance_sheet; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.balance_sheet (
    balance_sheet_id integer NOT NULL,
    ric text NOT NULL,
    cash_and_due_from_banks double precision NOT NULL,
    net_loans double precision NOT NULL,
    other_earning_assets double precision NOT NULL,
    total_assets double precision NOT NULL,
    total_deposits double precision NOT NULL,
    total_equity double precision NOT NULL,
    year integer NOT NULL,
    currency_id integer NOT NULL
);


ALTER TABLE public.balance_sheet OWNER TO postgres;

--
-- Name: currency; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.currency (
    currency_id integer NOT NULL,
    currency_name text NOT NULL
);


ALTER TABLE public.currency OWNER TO postgres;

--
-- Name: general_info; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.general_info (
    ric text NOT NULL,
    bank_name text NOT NULL,
    country_id integer NOT NULL,
    country_name text NOT NULL
);


ALTER TABLE public.general_info OWNER TO postgres;

--
-- Name: income_statement; Type: TABLE; Schema: public; Owner: postgres
--

CREATE TABLE public.income_statement (
    income_statement_id integer NOT NULL,
    ric text NOT NULL,
    interest_income double precision NOT NULL,
    net_interest_income double precision NOT NULL,
    non_interest_income double precision NOT NULL,
    total_interest_expense double precision NOT NULL,
    year integer NOT NULL,
    currency_id integer NOT NULL
);


ALTER TABLE public.income_statement OWNER TO postgres;

--
-- Data for Name: balance_sheet; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.balance_sheet (balance_sheet_id, ric, cash_and_due_from_banks, net_loans, other_earning_assets, total_assets, total_deposits, total_equity, year, currency_id) FROM stdin;
\.


--
-- Data for Name: currency; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.currency (currency_id, currency_name) FROM stdin;
\.


--
-- Data for Name: general_info; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.general_info (ric, bank_name, country_id, country_name) FROM stdin;
\.


--
-- Data for Name: income_statement; Type: TABLE DATA; Schema: public; Owner: postgres
--

COPY public.income_statement (income_statement_id, ric, interest_income, net_interest_income, non_interest_income, total_interest_expense, year, currency_id) FROM stdin;
\.


--
-- Name: balance_sheet balance_sheet_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.balance_sheet
    ADD CONSTRAINT balance_sheet_pkey PRIMARY KEY (balance_sheet_id);


--
-- Name: currency currency_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.currency
    ADD CONSTRAINT currency_pkey PRIMARY KEY (currency_id);


--
-- Name: general_info general_info_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.general_info
    ADD CONSTRAINT general_info_pkey PRIMARY KEY (ric);


--
-- Name: income_statement income_statement_pkey; Type: CONSTRAINT; Schema: public; Owner: postgres
--

ALTER TABLE ONLY public.income_statement
    ADD CONSTRAINT income_statement_pkey PRIMARY KEY (income_statement_id);


--
-- Name: SCHEMA public; Type: ACL; Schema: -; Owner: postgres
--

REVOKE ALL ON SCHEMA public FROM PUBLIC;
REVOKE ALL ON SCHEMA public FROM postgres;
GRANT ALL ON SCHEMA public TO postgres;
GRANT ALL ON SCHEMA public TO PUBLIC;


--
-- PostgreSQL database dump complete
--

