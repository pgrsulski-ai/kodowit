-- Prywatne migawki źródeł; osobne od publicznych aplikacji.
create table public.kodowit_sources (
 id uuid primary key default gen_random_uuid(),
 owner uuid not null default auth.uid() references auth.users(id) on delete cascade,
 name text not null check (char_length(name) between 1 and 100),
 version text not null check (version ~ '^[0-9]{1,5}\.[0-9]{1,5}\.[0-9]{1,5}$'),
 project jsonb not null check (jsonb_typeof(project)='object' and octet_length(project::text)<=500000),
 created_at timestamptz not null default now(),
 unique(owner,name,version)
);
alter table public.kodowit_sources enable row level security;
revoke all on public.kodowit_sources from public, anon, authenticated;
grant select, delete on public.kodowit_sources to authenticated;
grant insert(name,version,project) on public.kodowit_sources to authenticated;
create policy source_read on public.kodowit_sources for select to authenticated using (owner=auth.uid());
create policy source_insert on public.kodowit_sources for insert to authenticated with check (owner=auth.uid());
create policy source_delete on public.kodowit_sources for delete to authenticated using (owner=auth.uid());
create function public.kodowit_source_quota() returns trigger language plpgsql security definer set search_path='' as $$
begin
 perform pg_catalog.pg_advisory_xact_lock(130,1);
 if (select count(*) from public.kodowit_sources)>=100 then raise exception 'Globalny limit zapisów'; end if;
 if (select count(*) from public.kodowit_sources where owner=new.owner)>=10 then raise exception 'Limit 10 zapisów'; end if;
 return new;
end; $$;
revoke all on function public.kodowit_source_quota() from public;
create trigger source_quota before insert on public.kodowit_sources for each row execute function public.kodowit_source_quota();
