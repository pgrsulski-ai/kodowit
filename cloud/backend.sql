-- Uruchomić raz w SQL Editor własnego projektu Supabase.
create table public.kodowit_apps (
 id uuid primary key default gen_random_uuid(),
 owner uuid not null default auth.uid() references auth.users(id) on delete cascade,
 name text not null check (char_length(name) between 1 and 100),
 version text not null check (version ~ '^[0-9]{1,5}\.[0-9]{1,5}\.[0-9]{1,5}$'),
 html text not null check (octet_length(html) <= 500000),
 created_at timestamptz not null default now()
);
alter table public.kodowit_apps enable row level security;
revoke all on public.kodowit_apps from anon, authenticated;
grant select (id,name,version,html,created_at) on public.kodowit_apps to anon, authenticated;
grant insert (name,version,html), delete on public.kodowit_apps to authenticated;
create policy public_read on public.kodowit_apps for select using (true);
create policy own_insert on public.kodowit_apps for insert to authenticated with check (owner = auth.uid());
create policy own_delete on public.kodowit_apps for delete to authenticated using (owner = auth.uid());
create function public.kodowit_quota() returns trigger language plpgsql security definer set search_path = '' as $$
begin
 perform pg_catalog.pg_advisory_xact_lock(127, 1);
 if (select count(*) from public.kodowit_apps)>=100 then raise exception 'Globalny limit 100 publikacji'; end if;
 if (select count(*) from public.kodowit_apps where owner=new.owner)>=5 then raise exception 'Limit 5 publikacji'; end if;
 return new;
end; $$;
revoke all on function public.kodowit_quota() from public;
create trigger kodowit_quota before insert on public.kodowit_apps for each row execute function public.kodowit_quota();

-- RC129: zarządzanie wyłącznie własnymi publikacjami.
create or replace function public.kodowit_my_apps() returns table(id uuid,name text,version text,created_at timestamptz) language sql stable security definer set search_path = '' as $$
 select a.id,a.name,a.version,a.created_at from public.kodowit_apps a where a.owner=auth.uid() order by a.created_at desc;
$$;
create or replace function public.kodowit_remove_app(app_id uuid) returns boolean language plpgsql security definer set search_path = '' as $$
begin
 delete from public.kodowit_apps where id=app_id and owner=auth.uid(); return found;
end; $$;
create or replace function public.kodowit_update_app(app_id uuid,app_name text,app_version text,app_html text) returns boolean language plpgsql security definer set search_path = '' as $$
begin
 update public.kodowit_apps set name=app_name,version=app_version,html=app_html where id=app_id and owner=auth.uid(); return found;
end; $$;
revoke all on function public.kodowit_my_apps(), public.kodowit_remove_app(uuid), public.kodowit_update_app(uuid,text,text,text) from public, anon;
grant execute on function public.kodowit_my_apps(), public.kodowit_remove_app(uuid), public.kodowit_update_app(uuid,text,text,text) to authenticated;
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
-- Historia poprzednich publikacji: maks. 2 migawki na aplikację.
create table public.kodowit_app_history (
 id uuid primary key default gen_random_uuid(),
 app_id uuid not null references public.kodowit_apps(id) on delete cascade,
 name text not null, version text not null, html text not null check(octet_length(html)<=500000),
 saved_at timestamptz not null default clock_timestamp()
);
alter table public.kodowit_app_history enable row level security;
revoke all on public.kodowit_app_history from public, anon, authenticated;
create function public.kodowit_archive_app() returns trigger language plpgsql security definer set search_path='' as $$
begin
 if (old.name,old.version,old.html) is distinct from (new.name,new.version,new.html) then
 insert into public.kodowit_app_history(app_id,name,version,html) values(old.id,old.name,old.version,old.html);
 delete from public.kodowit_app_history where app_id=old.id and id not in (select h.id from public.kodowit_app_history h where h.app_id=old.id order by h.saved_at desc,h.id desc limit 2);
 end if;
 return new;
end; $$;
revoke all on function public.kodowit_archive_app() from public, anon, authenticated;
create trigger archive_app before update on public.kodowit_apps for each row execute function public.kodowit_archive_app();
create function public.kodowit_app_versions(target uuid) returns table(id uuid,name text,version text,saved_at timestamptz) language sql stable security definer set search_path='' as $$
 select h.id,h.name,h.version,h.saved_at from public.kodowit_app_history h join public.kodowit_apps a on a.id=h.app_id where a.id=target and a.owner=auth.uid() order by h.saved_at desc,h.id desc;
$$;
create function public.kodowit_restore_app(target uuid,snapshot uuid) returns boolean language plpgsql security definer set search_path='' as $$
declare previous public.kodowit_app_history%rowtype;
begin
 perform 1 from public.kodowit_apps where id=target and owner=auth.uid() for update;
 if not found then return false; end if;
 select * into previous from public.kodowit_app_history where id=snapshot and app_id=target;
 if not found then return false; end if;
 update public.kodowit_apps set name=previous.name,version=previous.version,html=previous.html where id=target and owner=auth.uid();
 return found;
end; $$;
revoke all on function public.kodowit_app_versions(uuid),public.kodowit_restore_app(uuid,uuid) from public, anon;
grant execute on function public.kodowit_app_versions(uuid),public.kodowit_restore_app(uuid,uuid) to authenticated;
