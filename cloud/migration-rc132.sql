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
